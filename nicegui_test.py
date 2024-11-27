from nicegui import ui
from typing import Dict
import time

### VARIABLES

message_list = [
    {
        "role": "assistant",
        "content": "Placeholder test"
    },
    {
        "role": "user",
        "content": "Placeholder test allso"
    },
    {
        "role": "assistant",
        "content": "no way, that's what i was gonna say"
    }
]

column_definitions = [
    {'name': 'thumbnail', 'label': 'Thumbnail', 'field': 'thumbnail'},
    {'name': 'id', 'label': 'ID', 'field': 'id'},
    {'name': 'name', 'label': 'Name', 'field': 'name'},
    {'name': 'status', 'label': 'Status', 'field': 'status'},
    {'name': 'spend', 'label': 'Spend', 'field': 'spend', 'sortable': True},
    {'name': 'email', 'label': 'Email', 'field': 'email'},
    {'name': 'phone', 'label': 'Phone', 'field': 'phone'},
    {'name': 'address', 'label': 'Address', 'field': 'address'},
]

rows = [
    {'id': 'ADID67', 'name': 'Alice', 'status': 'active', "thumbnail": "https://via.placeholder.com/150"},
    {'id': 'ADID68', 'name': 'Bob', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "spend": 100},
    {'id': 'ADID70', 'name': 'pee pee poo poo', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "spend": 99},
    {'id': 'ADID69', 'name': 'Charlie', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 1", "new_column_2": "Data 2"},
    {'id': 'ADID70', 'name': 'David', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 3", "new_column_2": "Data 4"},
    {'id': 'ADID71', 'name': 'Eve', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 5", "new_column_2": "Data 6"},
]



default_table_data = {
    'id': 1,
    'table_name': 'thick gurls',
    'rows': [
        {'id': 'ADID67', 'name': 'Alice', 'status': 'active', "thumbnail": "https://via.placeholder.com/150"},
        {'id': 'ADID68', 'name': 'Bob', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "spend": 100},
    ]
}

tables_data = [default_table_data]




### FUNCTIONS
def chat_window():
    scroll_area = None  # Initialize scroll_area to None

    def on_click(text_input):
        user_message = text_input.value
        if user_message:
            # Append the user input to the message_list
            message_list.append({"role": "user", "content": user_message})
            # Clear the text input
            text_input.value = ''
            # Refresh the chat window
            display_chat_messages.refresh()
            # Simulate sending the message to the backend and receiving a response
            response = {"role": "assistant", "content": "This is a response from the backend."}
            message_list.append(response)
            # Refresh the chat window again
            display_chat_messages.refresh()
            # Scroll to the bottom of the chat window
            if scroll_area:
                scroll_area.scroll_to(percent=1)

    @ui.refreshable
    def display_chat_messages():
        nonlocal scroll_area  # Declare scroll_area as nonlocal to modify it
        with ui.scroll_area().classes('w-full h-[70vh] border') as scroll_area:
            with ui.column().classes('w-full h-full items-stretch'):
                for message in message_list:
                    if message['role'] == 'user':
                        ui.label(f"{message['role']}: {message['content']}").classes('ml-auto my-2')
                    else:
                        ui.label(f"{message['role']}: {message['content']}").classes('mr-auto my-2')

    def text_input():
        with ui.column().classes('w-full mb-4 pb-4'):
            with ui.row().classes('w-full no-wrap items-center mb-4'):
                text = ui.input(placeholder='Type your message here...').props('rounded outlined input-class=mx-3') \
                    .classes('flex-grow')
                ui.button('Submit', on_click=lambda: on_click(text))
                # Add an event listener for the Enter key
                text.on('keydown.enter', lambda: on_click(text))

    with ui.column().classes('w-full h-full items-stretch'):
        ui.label('Chat Window').classes('text-center text-xl my-4')
        display_chat_messages()
        text_input()

def data_table_element(table_data):

    # create a column list from the items in the rows
    columns = [col for col in table_data['rows'][0].keys()]
    # use these collums to pick collumns form the column definitions
    visible_columns = [col for col in column_definitions if col['name'] in columns]


    def toggle(column: Dict, visible: bool) -> None:
        column['visible'] = visible
        # Update the visible_columns list based on the new visibility status
        if visible:
            if column not in visible_columns:
                visible_columns.append(column)
        else:
            visible_columns[:] = [col for col in visible_columns if col['name'] != column['name']]
        table.update()  # Refresh the table to reflect changes

    def column_toggle_menu():
        with ui.button(icon='menu'):
            with ui.menu(), ui.column().classes('gap-0 p-2'):
                for column in column_definitions:
                    is_visible = column in visible_columns
                    ui.switch(column['label'], value=is_visible, on_change=lambda e, column=column: toggle(column, e.value))

    def remove_table():
        tables_data.remove(table_data)
        display_tables.refresh()

    with ui.column().classes('mx-2'):
        with ui.row().classes('w-full justify-between items-center'):
            ui.label(table_data['table_name']).classes('text-lg my-2 font-bold')
            with ui.row().classes('gap-2'):
                column_toggle_menu()
                ui.button(icon='delete', on_click=remove_table).classes('text-red-500')

        # Filter columns based on visibility
        table = ui.table(columns=visible_columns, rows=table_data['rows'], row_key='name').classes('w-96')
        table.add_slot('body-cell-thumbnail', '''
            <q-td key="thumbnail" :props="props">
                <q-img :src="props.value" :ratio="1" />
            </q-td>
        ''')
    return table

def add_table():
    # Find the next available ID
    existing_ids = {table['id'] for table in tables_data}
    new_id = 1
    while new_id in existing_ids:
        new_id += 1
    
    # Append new table data with the unique ID
    tables_data.append(default_table_data)
    display_tables.refresh()

@ui.refreshable
def display_tables():
    with ui.row().classes('w-full overflow-x-auto'):
        for table_data in tables_data:
            with ui.column().classes('mx-2'):
                data_table_element(table_data)


### PAGES 
@ui.page('/')
def main():
    ui.dark_mode().enable()
    with ui.row().classes('w-full h-full items-stretch no-wrap'):
        with ui.column().classes('w-1/4 h-full'):
            chat_window()
        with ui.column().classes('w-3/4 h-full'):
            ui.button('Add Table', on_click=add_table).classes('mb-4')
            display_tables()

ui.run()