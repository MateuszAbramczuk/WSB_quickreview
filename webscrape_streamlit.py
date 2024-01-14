!pip install streamlit
!pip install pandas
!pip install plotly

import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

data = pd.read_excel("data_streamlit.xlsx", sheet_name=None)

st.set_page_config(page_title='WSB Quickreview', page_icon=":rocket:")

st.title("WallStreetBets 06.2020 - 12.2020 quickreview")

st.sidebar.markdown("## Select month or Stock")

st.markdown('<br><div style="height: 8px;"></div>', unsafe_allow_html=True)


select_event = st.sidebar.selectbox('How do you want to sort information?',
                                    ['Month', 'Stock Symbol'])

if select_event == 'Month':
    month_names =['June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = st.sidebar.selectbox('Select a Month', month_names)

    # Creating simple information
    monthly_users = data["posts_users_table"][data["posts_users_table"]['month'] == (month_names.index(month) + 6)]["author"].iloc[0]
    monthly_users_stock = data["posts_users_table_stocks"][data["posts_users_table_stocks"]["month"] == (month_names.index(month) + 6)]["author"].iloc[0]

    # Creating information about % change
    data["posts_users_table_per"].fillna(0, inplace=True)
    data["posts_users_table_stocks_per"].fillna(0, inplace=True)
    posts_users_table_per = data["posts_users_table_per"][data["posts_users_table_per"]['month'] == (month_names.index(month) + 6)]["author"].iloc[0]
    posts_users_table_stocks_per = data["posts_users_table_stocks_per"][data["posts_users_table_stocks_per"]["month"] == (month_names.index(month) + 6)]["author"].iloc[0]

    if posts_users_table_per > 0:
        color1 = 'green'
    elif posts_users_table_per < 0:
        color1 = 'red'
    else:
        color1 = 'white'
    
    if posts_users_table_stocks_per > 0:
        color2 = 'green'
    elif posts_users_table_stocks_per < 0:
        color2 = 'red'
    else:
        color2 = 'white'

    st.markdown(f"<div style='font-size: 30px;'>Monthly active posting users: <span style='color: #1a75ff;'>{monthly_users}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 20px;'>Percentage change from last month: <span style='color: {color1};'>{posts_users_table_per:.2%}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 30px;'>Monthly active users posting about stocks: <span style='color: #99e6ff;'>{monthly_users_stock}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 20px;'>Percentage change from last month: <span style='color: {color2};'>{posts_users_table_stocks_per:.2%}</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 15px;'>Values above are based on unique user names that were used during selected period of time</div>", unsafe_allow_html=True)
    st.markdown('<br><div style="height: 10px;"></div>', unsafe_allow_html=True)

    # Creating pie chart
    selected_month = (month_names.index(month) + 6)
    top_30 = data["top_in_all"][data["top_in_all"]["month"] == (month_names.index(month) + 6)]["top_30"].iloc[0]
    remaining = data["top_in_all"][data["top_in_all"]["month"] == (month_names.index(month) + 6)]["all"].iloc[0] - top_30
    pie_data1 = [
    {'category': 'Top 30', 'value': top_30},
    {'category': 'Remaining', 'value': remaining}
    ]
    fig1 = go.Figure(data=[go.Pie(labels=[d['category'] for d in pie_data1],
                             values=[d['value'] for d in pie_data1],
                             marker=dict(colors=['#ffbb99', '#ff7733'],
                                         line=dict(color='#ff9966', width=4)),
                             hole=0.3,
                             textinfo='percent+label',
                             pull=[0.08, 0])])
    fig1.update_layout(
        title_text=f'Proportion of Top 30 in Total',
        title_font_size=15,
        title_x=0.235,
        showlegend=False,
    )

    total_users = data["posts_users_table"][data["posts_users_table"]['month'] == (month_names.index(month) + 6)]["author"].iloc[0]
    stock_users = data["posts_users_table_stocks"][data["posts_users_table_stocks"]['month'] == (month_names.index(month) + 6)]["author"].iloc[0]

    # Prepare data for the pie chart
    pie_data2 = [
        {'category': 'Stock Users', 'value': stock_users},
        {'category': 'Other Users', 'value': total_users - stock_users}
    ]

    # Create the pie chart
    fig2 = go.Figure(data=[go.Pie(labels=[d['category'] for d in pie_data2],
                                 values=[d['value'] for d in pie_data2],
                                 marker=dict(colors=['#99e6ff', '#1a75ff'],
                                             line=dict(color='#4db8ff', width=4)),
                                 hole=0.3,
                                 textinfo='percent+label',
                                 pull=[0.08, 0])])
    
    fig2.update_layout(
        title_text=f'Proportion of Users Posting About Stocks',
        title_font_size=15,
        title_x=0.1,
        showlegend=False,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.plotly_chart(fig1, use_container_width=True)

    month_barchart = data["monthly_graphs"][data["monthly_graphs"]["month"] == (month_names.index(month) + 6)]

    fig3 = go.Figure(data=[
        go.Bar(
            x=month_barchart['tickers'], 
            y=month_barchart['values'], 
            marker_color='#ffaa80'  # Custom color
        )
    ])
    fig3.update_layout(
        title=f'Top Tickers for month number {month}',
        xaxis_title="Company's shortcut",
        yaxis_title='Value',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color="#80bfff"),
        xaxis=dict(tickangle=45)
    )
    fig3.update_traces(
     hovertemplate="<b>%{x}</b><br>Value: %{y}",
        hoverinfo='all'  # Show all hover info
    )
    st.plotly_chart(fig3)
elif select_event == 'Stock Symbol':
    month_names = {6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    top_30_all_time = list(pd.DataFrame(data["posts_title_table"].sum().sort_values(ascending=False)[:30]).index)
    stock = st.sidebar.selectbox("Select Company's Sumbol", top_30_all_time)

    # Creating barchart for Stock symbols based on values
    stock_barchart1 = data["posts_title_table"][["month",f"{stock}"]]
    stock_barchart1['month'] = stock_barchart1['month'].map(month_names)
    fig4 = go.Figure(data=[
        go.Bar(
            x=stock_barchart1["month"],
            y=stock_barchart1[f"{stock}"],
            marker_color='#33d6ff'
        )
    ])
    fig4.update_layout(
        title=f'Number of mentions in posts each month for company: {stock}',
        title_font_size=20,
        xaxis_title="Month",
        yaxis_title='Value',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color="#80bfff")
    )
    fig4.update_traces(
     hovertemplate="<b>%{x}</b><br>Value: %{y}",
        hoverinfo='x'
    )


    stock_barchart2 = data["posts_title_table_per_row"][["month",f"{stock}"]]
    stock_barchart2['month'] = stock_barchart2['month'].map(month_names)
    fig5 = go.Figure(data=[
        go.Bar(
            x=stock_barchart2["month"],
            y=stock_barchart2[f"{stock}"],
            marker_color='#b366ff'
        )
    ])
    fig5.update_layout(
        title=f'Percent of the {stock} in all stocks mentioned this month',
        title_font_size=20,
        xaxis_title="Month",
        yaxis_title='Percentage [%]',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color="#80bfff")
    )
    fig5.update_traces(
     hovertemplate="<b>%{x}</b><br>Value: %{y}",
        hoverinfo='x'
    )

    st.plotly_chart(fig4)
    st.plotly_chart(fig5)
    pass
