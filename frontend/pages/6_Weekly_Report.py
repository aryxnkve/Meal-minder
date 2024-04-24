import streamlit as st
import numpy as np
import io
from datetime import datetime
from services import backend
import uuid
from dotenv import load_dotenv


from streamlit_extras.let_it_rain import rain
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.graph_objects as go
import plotly
from matplotlib.colors import rgb2hex

load_dotenv()

st.set_page_config(
    page_title="Nutribuddy",
    page_icon="🌱",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

def call_backend():
    status, response = backend.get_report_data(st.session_state.auth_token)
    print("Got response from API", response)
    if status:
        return response
    else:
        return None

auth_user = authentication()
# auth_user = ("sayali")
if auth_user[0]:
    # implement here
    # st.balloons()
    
    # rain(
    #     emoji="🎖",
    #     font_size=54,
    #     falling_speed=5,
    #     animation_length="infinite",
    # )

    weekly_dishes = call_backend()

    ideal_daily_calories = 600  # Example value, adjust as needed


    # # Function to create a progress bar image
    # def create_progress_bar(dishes):
    #     fig, ax = plt.subplots(figsize=(4, 0.25))  # Wide and short figure
    #     colors = plt.cm.viridis(np.linspace(0, 1, len(dishes)))
    #     start = 0
    #     for (dish, calories), color in zip(dishes, colors):
    #         ax.barh(0, calories, left=start, color=color)
    #         start += calories
    #     ax.axis('off')  # Hide axes
    #     buf = BytesIO()
    #     plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    #     plt.close(fig)
    #     buf.seek(0)
    #     return buf

    # # Creating a dataframe
    # data = []
    # for day, dishes in weekly_dishes.items():
    #     dishes_str = ', '.join([f"{dish} ({cal} cal)" for dish, cal in dishes])
    #     progress_image = create_progress_bar(dishes)
    #     data.append([day, dishes_str, progress_image])

    # Function to create a progress bar image and return colors
    def create_progress_bar(dishes):
        fig, ax = plt.subplots(figsize=(4, 0.25))  # Wide and short figure
        total_calories = sum(cal for _, cal in dishes)
        colors = plt.cm.Wistia(np.linspace(0, 1, len(dishes)))
        start = 0
        for (dish, calories), color in zip(dishes, colors):
            if start + calories > ideal_daily_calories:
                color = 'red'  # Change color to red if going over the ideal calories
            ax.barh(0, calories, left=start, color=color, height=1)
            start += calories
        ax.set_xlim(0, max(total_calories, ideal_daily_calories))  # Adjust xlim to show overconsumption
        ax.axis('off')  # Hide axes
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        buf.seek(0)
        return buf, colors


    # Creating a dataframe
    data = []
    for day, dishes in weekly_dishes.items():
        progress_image, colors = create_progress_bar(dishes)
        # Prepare dishes string with HTML color tags
        dishes_str = ', '.join([f"<span style='color:{rgb2hex(color)};'>{dish} ({cal} cal)</span>" for (dish, cal), color in zip(dishes, colors)])
        data.append([day, dishes_str, progress_image])



    df = pd.DataFrame(data, columns=['Day', 'Dishes', 'Progress'])

    # Calculate total daily calories and prepare data for the charts
    days = list(weekly_dishes.keys())
    total_daily_calories = [sum(cal for _, cal in dishes) for dishes in weekly_dishes.values()]
    total_weekly_calories = sum(total_daily_calories)
    ideal_weekly_calories = 14000  # Example ideal calories, adjust as necessary

    # # Create line chart for daily calories
    # fig1, ax1 = plt.subplots()
    # fig1.patch.set_facecolor('black')
    # ax1.plot(days, total_daily_calories, marker='o', linestyle='-', color='r')
    # ax1.set_facecolor('black')
    # ax1.xaxis.label.set_color('white')
    # ax1.yaxis.label.set_color('white')
    # ax1.tick_params(axis='x', colors='white')
    # ax1.tick_params(axis='y', colors='white')
    # ax1.set_xlabel('Day of the Week')
    # ax1.set_ylabel('Calories')
    # ax1.set_title('Daily Calorie Intake')

    # # Create donut chart for weekly calories
    # fig2, ax2 = plt.subplots()
    # fig2.patch.set_facecolor('black')
    # ax2.pie([total_weekly_calories, ideal_weekly_calories - total_weekly_calories], labels=['Consumed', 'Remaining'], startangle=90, colors=['#ff9999','#66b3ff'], autopct='%1.1f%%', pctdistance=0.85)
    # ax2.add_artist(plt.Circle((0,0),0.70,fc='black'))
    # ax2.set_title('Weekly Calorie Intake vs Ideal', color='white')


    # Create an interactive line chart for daily calories
    def create_line_chart(days, calories):
        trace = go.Scatter(
            x=days,
            y=calories,
            mode='lines+markers',
            marker=dict(size=8),  # Adjust marker size for better visibility
            line=dict(width=2),  # Line width
            hoverinfo='y',  # Show only the y value on hover
        )
        
        layout = go.Layout(
            title='Daily Calorie Intake',
            xaxis=dict(title='Day of the Week'),
            yaxis=dict(title='Calories'),
            paper_bgcolor='black',  # Set background color to white
            plot_bgcolor='black',  # Ensure plot background is also white
            font=dict(color='white'),
            shapes=[
                # Line Horizontal Ideal Calorie Limit
                dict(
                    type='line',
                    xref='paper', x0=0, x1=1,  # Spanning the entire x-axis
                    yref='y', y0=ideal_daily_calories, y1=ideal_daily_calories,
                    line=dict(
                        color='red',
                        width=2,
                        dash='dot',  # Dotted line style
                    ),
                )
            ]
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        return fig

    # Creating the line chart
    line_chart = create_line_chart(days, total_daily_calories)




    # Create an interactive donut chart
    def create_donut_chart(total_calories, ideal_calories):
        labels = ['Consumed', 'Remaining']
        values = [total_calories, ideal_calories - total_calories]
        colors = ['#1f77b4', 'black']  # Color for consumed and remaining calories
        
        trace = go.Pie(labels=labels, values=values, hole=0.6, marker=dict(colors=colors, line=dict(color='white', width=2)),
                    hoverinfo='label+value', textinfo='none')
        
        layout = go.Layout(
            title='Weekly Calorie Intake vs Ideal',
            showlegend=True,
            paper_bgcolor='black',  # Set chart background color
            plot_bgcolor='black',
            font=dict(color='white')
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        return fig

    # Creating the donut chart
    donut_chart = create_donut_chart(total_weekly_calories, ideal_weekly_calories)


    # Streamlit app
    st.title('Weekly Tracker')
    st.write('This table shows what you ate each day and visualizes the calorie intake.')

    # Display the dataframe and images
    # Define header
    col1, col2, col3 = st.columns([1, 3, 3])
    col1.subheader("Day")
    col2.subheader("Dishes")
    col3.subheader("Progress")
    for index, row in df.iterrows():
        cols = st.columns([1, 3, 2])
        cols[0].write(row['Day'])
        cols[1].write(row['Dishes'], unsafe_allow_html=True)
        cols[2].image(row['Progress'], use_column_width=True)

   
    # Display charts side by side in Streamlit
    col1, col2 = st.columns(2)
    with col1:
        # Display the interactive line chart
        st.plotly_chart(line_chart, use_container_width=True)
        # st.pyplot(fig1)

    with col2:
        # Display the interactive donut chart
        st.plotly_chart(donut_chart, use_container_width=True)
        # st.pyplot(fig2)

else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
