from .models import WorkflowSession, Workflow
import json

class WorkflowEngine:
    @staticmethod
    def process_workflow(client, phone_number, incoming_text):
        """
        Process the incoming text to advance an active workflow session,
        or start a new workflow session if a trigger matches.
        Returns the (text_response, buttons_response) to send, or (None, None) if no workflow logic applies.
        """
        incoming_text_lower = incoming_text.lower().strip()

        # 1. Check for active session
        session = WorkflowSession.objects.filter(
            client=client, 
            phone_number=phone_number, 
            is_active=True
        ).first()

        if session:
            # Advance the existing session
            return WorkflowEngine._advance_session(session, incoming_text)

        # 2. Check for new workflow triggers
        workflows = Workflow.objects.filter(client=client, enabled=True, trigger_type='KEYWORD')
        for wf in workflows:
            if isinstance(wf.trigger_value, list):
                # Ensure lowercase comparison
                trigger_keywords = [t.lower() for t in wf.trigger_value]
                if incoming_text_lower in trigger_keywords:
                    # Found a matching workflow, start it!
                    return WorkflowEngine._start_workflow(client, phone_number, wf)
            elif isinstance(wf.trigger_value, str):
                if incoming_text_lower == wf.trigger_value.lower():
                    return WorkflowEngine._start_workflow(client, phone_number, wf)

        return None, None

    @staticmethod
    def _start_workflow(client, phone_number, workflow):
        # Parse the JSON steps
        steps = workflow.steps
        if not steps or 'nodes' not in steps:
            return None, None
            
        nodes = steps.get('nodes', [])
        edges = steps.get('edges', [])

        # Find the trigger (start) node
        start_node = next((n for n in nodes if n.get('type') == 'trigger'), None)
        if not start_node:
            return None, None

        # Create session
        session = WorkflowSession.objects.create(
            client=client,
            phone_number=phone_number,
            workflow=workflow,
            current_node_id=start_node.get('id')
        )

        # Advance it immediately to get the first real message node
        return WorkflowEngine._advance_session(session, "")

    @staticmethod
    def _advance_session(session, incoming_text):
        steps = session.workflow.steps
        nodes = steps.get('nodes', [])
        edges = steps.get('edges', [])
        
        current_node_id = session.current_node_id
        current_node = next((n for n in nodes if n.get('id') == current_node_id), None)
        
        if not current_node:
            session.is_active = False
            session.save()
            return None, None

        # Determine which edge to follow
        next_edge = None

        if current_node.get('type') == 'buttons':
            # We must match the user's text exactly with one of the buttons
            buttons = current_node.get('data', {}).get('buttons', [])
            matched_index = -1
            for i, btn_text in enumerate(buttons):
                if incoming_text.strip().lower() == btn_text.lower():
                    matched_index = i
                    break
            
            if matched_index != -1:
                source_handle = f"btn-{matched_index}"
                # Find edge with this sourceHandle
                next_edge = next((e for e in edges if e.get('source') == current_node_id and e.get('sourceHandle') == source_handle), None)
            else:
                # If they typed something else, repeat the current node (don't advance)
                return WorkflowEngine._get_node_response(current_node)
                
        else:
            # For plain nodes or trigger nodes, just follow the first available edge
            next_edge = next((e for e in edges if e.get('source') == current_node_id), None)

        if not next_edge:
            # End of workflow reached
            session.is_active = False
            session.save()
            return None, None

        # Move to the target node
        next_node_id = next_edge.get('target')
        next_node = next((n for n in nodes if n.get('id') == next_node_id), None)

        if not next_node:
            session.is_active = False
            session.save()
            return None, None

        # Update session
        session.current_node_id = next_node_id
        session.save()

        # If the next node is also a routing node without a message (unlikely in this UI), we'd recurse.
        # But based on the templateData, all target nodes have messages.
        return WorkflowEngine._get_node_response(next_node)

    @staticmethod
    def _get_node_response(node):
        data = node.get('data', {})
        message = data.get('message', '')
        buttons = data.get('buttons', [])
        return message, buttons
