import streamlit as st
import asyncio
import httpx
import json
import time
from rag_utility import generate_data_store, query_rag
import os
from dotenv import load_dotenv
from httpx import Timeout
import traceback
from streamlit_calendar import calendar
from datetime import datetime

load_dotenv()

working_dir = os.path.dirname(os.path.abspath(__file__))
datapath = "docs"
if not os.path.exists(os.path.join(working_dir, datapath)):
    os.mkdir(os.path.join(working_dir, datapath))

API_URL = "http://localhost:8000/chat/stream"

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'label_visibility' not in st.session_state:
    st.session_state.label_visibility = "visible"
if 'model_type' not in st.session_state:
    st.session_state.model_type = "openai"

if 'pdf_docs' not in st.session_state:
    st.session_state.pdf_docs = []

if 'pdf_mode' not in st.session_state:
    st.session_state.pdf_mode = False

def find_key(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            result = find_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None

def format_message(message):
    if message['role'] == 'user':
        return {
            "content": message['content'],
            "additional_kwargs": {},
            "response_metadata": {},
            "type": "human",
            "name": "string",
            "id": "string",
            "example": False,
            "additionalProp1": {}
        }
    else:
        return {
            "content": message['content'],
            "additional_kwargs": {},
            "response_metadata": {},
            "type": "ai",
            "name": "string",
            "id": "string",
            "example": False,
            "additionalProp1": {}
        }
    
async def chat_with_bot(user_input):
    messages = list(map(format_message, st.session_state.messages)) if st.session_state.messages else []
    # messages.append({
    #       "content": user_input,
    #         "additional_kwargs": {},
    #         "response_metadata": {},
    #         "type": "ai",
    #         "name": "string",
    #         "id": "string",
    #         "example": False,
    #         "additionalProp1": {}
    # })

    input_json = {
                "input": {
                "messages": messages,
            },
            "config": {
                "configurable": {
                "model_name":st.session_state.model_type,
                }
            },
            "kwargs": {}
    }

    timeout = Timeout(10.0, read=300.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            async with client.stream("POST", API_URL, json=input_json) as response:
                if response.status_code == 200:
                    full_response = ""
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        full_response = ""
                        last_event = None
                        
                        async for line in response.aiter_lines():
                            if line and line.startswith("event: "):
                                event_type = line.replace("event: ", "").strip()
                                continue
                            
                            if line and line.startswith("data: "):
                                chunk_json = json.loads(line[6:])
                                last_event = chunk_json  # Store the current event
                                
                                # Handle intent node
                                if "intent_node" in chunk_json:
                                    intent = chunk_json["intent_node"]["intent"]
                                    with st.expander("🎯 Intent", expanded=True):
                                        st.markdown(f"`{intent}`")
                                        st.session_state.messages.append({"role": "assistant", "content": intent, "type": "expander", "title":"🎯 Intent"})
                                
                                # Handle search node
                                elif "search_node" in chunk_json:
                                    messages = chunk_json["search_node"].get("messages", [])
                                    for msg in messages:
                                        if msg.get("tool_calls"):
                                            tool_call = msg["tool_calls"][0]
                                            if "function" in tool_call:
                                                tool_args = json.loads(tool_call["function"]["arguments"])
                                                with st.expander("🔍 Web Search Query", expanded=True):
                                                    st.markdown(f"`{tool_args.get('query', '')}`")
                                                    st.session_state.messages.append({"role": "assistant", "content": tool_args.get('query', ''), "type": "expander", "title":"🔍 Web Search Query"})
                                        else:
                                            with st.expander("🔍 Search Summary", expanded=True):
                                                st.markdown(f"`{msg.get('content', '')}`")
                                                st.session_state.messages.append({"role": "assistant", "content": msg.get('content', ''), "type": "expander", "title":"🔍 Search Summary"})
                                                

                                # Handle email send node
                                elif "email_send_node" in chunk_json:
                                    email_messages = chunk_json["email_send_node"].get("messages", [])
                                    for msg in email_messages:
                                        if msg.get("tool_calls"):
                                            tool_call = msg["tool_calls"][0]
                                            if "function" in tool_call:
                                                tool_args = json.loads(tool_call["function"]["arguments"])
                                                with st.expander("📧 Email Details", expanded=True):
                                                    email_details = f"""
                                                        **To:** {tool_args.get('recipient_email', 'N/A')}
                                                        **Subject:** {tool_args.get('subject', 'N/A')}
                                                        **Content:** {tool_args.get('body', 'N/A')}
                                                    """
                                                    st.markdown(email_details)
                                                st.session_state.messages.append({"role": "assistant", "content": email_details, "type": "expander", "title": "📧 Email Details"})
                                                
                                        else:
                                            with st.expander("📧 Email Information", expanded=True):
                                                response = msg.get('content', '').replace('FINAL ANSWER', '')
                                                st.markdown(response)
                                                st.session_state.messages.append({"role": "assistant", "content": response, "type": "expander", "title": "📧 Email Information"})
                                                

                                # Handle scheduler node
                                elif "scheduler_node" in chunk_json:
                                    scheduler_messages = chunk_json["scheduler_node"].get("messages", [])
                                    for msg in scheduler_messages:
                                        if msg.get("tool_calls"):
                                            tool_call = msg["tool_calls"][0]
                                            if "function" in tool_call:
                                                tool_args = json.loads(tool_call["function"]["arguments"])
                                                with st.expander("📅 Meeting Request", expanded=True):
                                                    meeting_details = f"""
                                                        **Title:** {tool_args.get('title', 'N/A')}
                                                        **Time:** {tool_args.get('time', 'N/A')}
                                                        **Duration:** {tool_args.get('duration', 'N/A')}
                                                        **Attendees:** {', '.join(tool_args.get('attendees', ['N/A']))}
                                                    """
                                                    st.markdown(meeting_details)
                                                    st.session_state.messages.append({"role": "assistant", "content": meeting_details, "type": "expander", "title": "📅 Meeting Request"})
                                                
                                        else:
                                            with st.expander("📅 Scheduler Response", expanded=True):
                                                response = msg.get('content')
                                                response = response.replace("FINAL ANSWER", "")
                                                st.markdown(response)
                                                st.session_state.messages.append({"role": "assistant", "content": response, "type": "expander", "title": "📅 Scheduler Response"})
                                                

                                # Handle tool node
                                elif "tool_node" in chunk_json:
                                    tool_messages = chunk_json["tool_node"].get("messages", [])
                                    for msg in tool_messages:
                                        if msg.get("type") == "tool":
                                            tool_name = msg.get("name", "unknown")
                                            tool_content = msg.get("content", "")
                                            if "email" in tool_name.lower():
                                                try:
                                                    response_data = json.loads(tool_content)
                                                    if "draft" in tool_name.lower() and response_data.get("successful"):
                                                        with st.expander("📧 Email Draft Created", expanded=True):
                                                            message = "Email draft created successfully!"
                                                            st.success(message)
                                                            st.session_state.messages.append({"role": "assistant", "content": message, "type": "expander-success", "title": "📧 Email Draft Created"})        
                                                    elif "send" in tool_name.lower():
                                                        response_data = json.loads(tool_content)
                                                        if response_data.get("successfull"):
                                                            with st.expander("📧 Email Tool Result", expanded=True):
                                                                message = "Email sent successfully!"
                                                                st.success(message)
                                                                st.session_state.messages.append({"role": "assistant", "content": message, "type": "expander-success", "title": "📧 Email Tool Result"})        
                                                        else:
                                                            with st.expander("📧 Email Tool Result", expanded=True):
                                                                message ="Failed to send email."
                                                                st.error(message)
                                                                st.session_state.messages.append({"role": "assistant", "content": message, "type": "expander-error", "title": "📧 Email Tool Result"})        
               
                                                except Exception as e:
                                                    print(e)
                                                    with st.expander("📧 Email Tool Result", expanded=True):
                                                        st.markdown(tool_content)
                                            elif "schedule" in tool_name.lower():
                                                try:
                                                    # Parse the response data
                                                    response_data = json.loads(tool_content)
                                                    if response_data.get("successfull") and response_data.get("data", {}).get("response_data"):
                                                        event = response_data["data"]["response_data"]
                                                        # Format the datetime strings
                                                        start_time = event["start"]["dateTime"]
                                                        end_time = event["end"]["dateTime"]
                                                        
                                                        # Format attendees list
                                                        attendees = ", ".join([att["email"] for att in event.get("attendees", [])])
                                                        
                                                        with st.expander("📅 Meeting Scheduled!", expanded=True):
                                                            message = f"""
                                                                    ✅ **Meeting Successfully Scheduled**
                                                                    
                                                                    **Title:** {event.get('summary')}
                                                                    **Date:** {start_time} to {end_time}
                                                                    **Attendees:** {attendees}
                                                                    **Organizer:** {event.get('organizer', {}).get('email')}
                                                                    
                                                                    [View in Calendar]({event.get('htmlLink')})
                                                                    """
                                                            st.markdown(message)
                                                            st.session_state['messages'].append({"role": "assistant", "content": message.strip(), "type": "expander", "title": "📅 Success"})
                                                    else:
                                                        with st.expander("📅 Error", expanded=True):
                                                            message = "Failed to schedule the meeting. Please try again."
                                                            st.error(message)
                                                        st.session_state['messages'].append({"role": "assistant", "content": message.strip(), "type": "expander-error", "title": "📅 Error"})
                                                except json.JSONDecodeError:
                                                    with st.expander("📅 Error", expanded=True):
                                                        message = "Failed to process scheduler response."
                                                        st.error(message)
                                                    st.session_state['messages'].append({"role": "assistant", "content": message.strip(), "type": "expander-error", "title": "📅 Error"})
                                            elif "search" in tool_name.lower():
                                                try:
                                                    # results = json.loads(tool_content)
                                                    with st.expander("🔍 Search Results", expanded=True):
                                                        st.markdown(
                                                            f'<div style="max-height: 300px; overflow-y: auto;">{tool_content}</div>',
                                                            unsafe_allow_html=True
                                                        )
                                                    st.session_state['messages'].append({"role": "assistant", "content": tool_content.strip(), "type": "expander", "title": "🔍 Search Results"})
                                                except Exception as e:
                                                    with st.expander("🔍 Search Results", expanded=True):
                                                        message = "failed to process search results"
                                                        st.error(message)
                                                        st.session_state['messages'].append({"role": "assistant", "content": message.strip(), "type": "expander-error", "title": "🔍 Search Results"})
                                else:
                                    # Handle regular content (LLM response)
                                    output_content = find_key(chunk_json, "content")
                                    if output_content is not None and output_content.strip():
                                        full_response += output_content
                                        if not any(node in last_event for node in ["intent_node", "search_node", "email_send_node", "scheduler_node", "tool_node"]):
                                            message_placeholder.markdown(full_response + "▌")
                                        else:
                                            with st.expander("🤖 Intermediate Response", expanded=True):
                                                st.markdown(full_response)
                                                st.session_state['messages'].append({"role": "assistant", "content": full_response.strip(), "type": "chat", "title": "🔍 Search Results"})
                        # Final message display (always in message_placeholder)
                        full_response = full_response.replace("FINAL ANSWER", "")
                        message_placeholder.markdown(full_response.strip())
                    
                    st.session_state['messages'].append({"role": "assistant", "content": full_response.strip(), "type": "chat"})
                else:
                    error_message = await response.aread()
                    st.error(f"Error: {error_message}")
        except httpx.ReadTimeout:
            st.error("ReadTimeout: The request took too long to process.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            traceback.print_exc()

# Add custom CSS at the top of the file
st.markdown(
    """
    <style>
    /* Top bar styling */
    .topbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #070738;
        display: flex;
        align-items: center;
        padding: 0 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    .topbar-title {
        font-size: 24px;
        font-weight: 600;
        color: white;
        margin-left: 50px;
    }
    
    /* Adjust main content to account for top bar */
    .main .block-container {
        padding-top: 80px !important;
    }
    
    /* Hide default header decoration */
    header {
        background-color: transparent !important;
    }
       
    # /* Hide the default title */
    # .stTitle {
    #     display: none;
    # }

    /* Ensure sidebar appears below the top bar */
    [data-testid=stSidebar] {
        margin-top: 10px;
        z-index: 100;

    }
    </style>
    <div class="topbar">
        <div class="topbar-title">SNOOZE</div>
    </div>
    """, 
    unsafe_allow_html=True
)

# st.title("SNOOZE")

with st.sidebar:
    # Create tabs for Calendar, To-Do List, and Emails
    tab1, tab2, tab3 = st.tabs(["📅 Calendar", "📝 To-Do List", "📧 Emails"])

    with tab1:
        calendar_options = {
            "editable": "true",
            "selectable": "true",
            "headerToolbar": {
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "initialView": "dayGridMonth",
        }
        calendar_events = [
            {
                "title": "Event 1",
                "start": "2024-11-19T08:30:00",
                "end": "2024-11-20T10:30:00",
                "resourceId": "a",
            },
            {
                "title": "Event 2",
                "start": "2023-07-31T07:30:00",
                "end": "2023-07-31T10:30:00",
                "resourceId": "b",
            },
            {
                "title": "Event 3",
                "start": "2023-07-31T10:40:00",
                "end": "2023-07-31T12:30:00",
                "resourceId": "a",
            }
        ]
        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """

        calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
        # st.view(calendar)

    with tab2:
        # To-Do List functionality
        if 'todo_list' not in st.session_state:
            st.session_state.todo_list = ["Test 1","Test 2","Test 3"]
        st.subheader("Your Tasks")
        # Display the current tasks in a Google Tasks-like format
        if st.session_state.todo_list:
            for idx, task in enumerate(st.session_state.todo_list, start=1):
                st.markdown(
                    f"""
                    <div style="padding: 8px; border-bottom: 1px solid #e0e0e0;">
                        <input type="checkbox" id="task-{idx}" style="margin-right: 10px;">
                        <label for="task-{idx}" style="cursor: pointer;">{task}</label>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(
                """
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write("No tasks in the list.")

    with tab3:
        st.markdown(
            """
            <div style="color: white; font-size: 18px;">
                <h3>Emails</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th style="border: 1px solid #ddd; padding: 8px;">Sender</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Subject</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 8px;">example@example.com</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">Sample Email Subject</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">2024-01-01</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 8px;">another@example.com</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">Another Email Subject</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">2024-01-02</td>
                        </tr>
                        <!-- Add more email rows as needed -->
                    </tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )

# Remove the subheader and replace with a cleaner prompt

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        content = message['content']  # Simplified content assignment
        if "expander" in message["type"]:
            with st.expander(message["title"], expanded=True):
                # Add a scroll box for the expander content

                if "success" in message["type"]:
                    st.success(content)
                elif "error" in message["type"]:
                    st.error(content)
                else:
                    st.markdown(
                    f"""
                    <div style="max-height: 300px; overflow-y: auto;">
                        {content}
                    </div>
                    """, 
                    unsafe_allow_html=True
                    )
        else:
            st.write(content)

if prompt := st.chat_input("You:"):
    # Add PDF context to the message if PDF mode is enabled
    st.session_state['messages'].append({"role": "user", "content": prompt, "type": "chat"})
    with st.chat_message("user"):
        st.markdown(prompt)
    if st.session_state.pdf_mode and st.session_state.pdf_docs:
        # prompt = f"Using the context from the upload PDF documents, please answer: {prompt}"
        formatted_response, response_text  = query_rag(prompt)
        with st.chat_message("assistant"):
            st.markdown(formatted_response["response"])
        st.session_state['messages'].append({"role": "assistant", "content": formatted_response["response"], "type": "chat"})
    elif st.session_state.pdf_mode and not st.session_state.pdf_docs:
        st.error("Please upload documents first to use document query mode!")
        st.stop()
    else:
        asyncio.run(chat_with_bot(prompt))
