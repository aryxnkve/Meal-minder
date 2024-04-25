import streamlit as st
import numpy as np
import io
from datetime import datetime
from services import backend
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

def get_report_api():
    status, response = backend.get_report_data(st.session_state.auth_token)
    print("Got response from API", response)
    if status:
        return response
    else:
        return None
    
def get_daily_calories():
    status, response = backend.get_user_daily_calories(st.session_state.auth_token)
    if status:
        return response
    else:
        print("Some error occurred", response)
        return 0

auth_user = authentication()


if auth_user[0]:
    # implement here
    # st.balloons()
    
    # rain(
    #     emoji="🎖",
    #     font_size=54,
    #     falling_speed=5,
    #     animation_length="infinite",
    # )

    weekly_dishes = get_report_api()
    ideal_daily_calories = get_daily_calories()
    ideal_weekly_calories = 7 * ideal_daily_calories
    # weekly_dishes= {
    #     'Monday': [('Pasta', 400), ('Salad', 150), ('Veggies', 100)],
    #     'Tuesday': [('Burger', 500), ('Fries', 300)],
    #     'Wednesday': [('Chicken', 350), ('Rice', 200)],
    #     'Thursday': [('Fish', 250), ('Veggies', 100)],
    #     'Friday': [('Pizza', 480), ('Ice Cream', 330)],
    #     'Saturday': [('Steak', 550), ('Potato', 220)],
    #     'Sunday': [('Sushi', 300), ('Soup', 150)]
    # }


    # Function to create a progress bar image and return colors
    def create_progress_bar(dishes):
        fig, ax = plt.subplots(figsize=(4, 0.25))  # Wide and short figure
        total_calories = sum(cal for _, cal in dishes)
        colors = plt.cm.Wistia(np.linspace(0, 1, len(dishes)))
        start = 0
        for (dish, calories), color in zip(dishes, colors):
            # if start + calories > ideal_daily_calories:
            #     color = 'red'  # Change color to red if going over the ideal calories
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
    total_sum = 0
    for day, dishes in weekly_dishes.items():
        total_sum = sum(cal for dish, cal in dishes)
        calorie_diff = ideal_daily_calories - total_sum
        if abs(calorie_diff) <= 50 or calorie_diff == 0:
            diff = f"✅ Goal acheived!"
        elif calorie_diff < 0 :
            diff = f"🔺 {abs(calorie_diff)} cal"
        elif calorie_diff > 0:
            diff = f"🔹 {calorie_diff} cal"
        dishes_str = ', '.join([f"{dish} ({cal} cal)" for dish, cal in dishes])

        # progress_image, colors = create_progress_bar(dishes)
        # Prepare dishes string with HTML color tags
        # dishes_str = ', '.join([f"<span style='color:{rgb2hex(color)};'>{dish} ({cal} cal)</span>" for (dish, cal), color in zip(dishes, colors)])
        data.append([day, dishes_str, total_sum, diff])



    df = pd.DataFrame(data, columns=['Day', 'Dishes', 'Progress', 'Calories'])
    # print(df)

    # Calculate total daily calories and prepare data for the charts
    days = list(weekly_dishes.keys())
    total_daily_calories = [sum(cal for _, cal in dishes) for dishes in weekly_dishes.values()]
    total_weekly_calories = sum(total_daily_calories)

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
            title=f'Daily Calorie Intake (Goal : {ideal_daily_calories})',
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
    col1, col2, col3, col4 = st.columns([1,2,2,1])
    col1.subheader("Day")
    col2.subheader("Dishes")
    col3.subheader("Progress")
    col4.subheader("Calories")
    for index, row in df.iterrows():
        cols = st.columns([1,2,2,1])
        cols[0].write(row['Day'])
        cols[1].write(row['Dishes'], unsafe_allow_html=True)
        print(row['Progress'])
        calorie_diff = ideal_daily_calories - row['Progress']
        print("calorie diff = ", calorie_diff)
        if abs(calorie_diff) <= 50 or calorie_diff == 0:
            display_val = f"{row['Progress']}/{ideal_daily_calories}"
            val = 100
        elif calorie_diff > 50 :
            display_val = f"{row['Progress']}/{ideal_daily_calories}"
            val = round((calorie_diff / ideal_daily_calories) * 100)
        elif calorie_diff < -50:
            display_val = f"{abs(row['Progress'])}/{ideal_daily_calories}"
            val = 100
        print(display_val, val)
        
        probar = cols[2].progress(0, text=display_val)
        probar.progress(val, text=display_val)

        # cols[2].image(row['Progress'], use_column_width=True)
        cols[3].write(row['Calories'])

   
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
