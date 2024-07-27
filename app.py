import streamlit as st
import pandas as pd
import plotly.express as px


class Dashboard:
    colors = {
        'first': '#6826e1',
        'second': '#5bb3e0',
        'third': '#e39ccd'
    }
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.df = self.add_datetime_features(self.df)
        self.january, self.february, self.march = 1, 2, 3
        self.df_january, self.df_february, self.df_march = self.filter_by_month(self.df)

        self.size = {
            'height': 346,
            'width': 400
        }

    def add_datetime_features(self, df):
        def categorize_time_of_day(hour):
            if 5 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 21:
                return 'Evening'
            else:
                return 'Night'

        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d-%m-%Y %H:%M:%S')
        df['Day'] = df['DateTime'].dt.day
        df['Month'] = df['DateTime'].dt.month
        df['TimeOfDay'] = df['DateTime'].dt.hour.apply(categorize_time_of_day)
        return df

    def filter_by_month(self, df):
        df_january = df[df['Month'] == self.january]
        df_february = df[df['Month'] == self.february]
        df_march = df[df['Month'] == self.march]
        return df_january, df_february, df_march

    def plot_bar_chart_1(self, df_current_month):
        city_color = {
            'Yangon': self.colors['first'],
            'Naypyitaw': self.colors['second'],
            'Mandalay': self.colors['third']
        }

        fig = px.bar(df_current_month, x='City', y='Revenue', title='Total Sales by City', color='City',
                     color_discrete_map=city_color)

        fig.update_traces(width=0.5)  # Set the width of the bars
        fig.update_layout(
            height=self.size['height'],
            width=self.size['width'],
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            bargap=0.4,
            title=dict(
                text='Total Sales by City',
                font=dict(
                    size=14
                )
            ),
            xaxis=dict(
                title=''  # Remove the x-axis title
            ),
            legend=dict(
                x=0.83,  # Adjust the x position
                y=1.2,  # Adjust the y position
                xanchor='center',  # Anchor the legend to the center
                yanchor='top',  # Anchor the legend to the top
                title=dict(
                    text=''  # Remove the legend title
                )
            )
        )
        fig.update_yaxes(range=[30000, 40000], dtick=2000)
        return fig

    def plot_bar_chart_2(self, df_current_month):
        grouped_data = df_current_month.groupby(['Product line', 'Payment method']).agg(
            {'Revenue': 'sum'}).reset_index()

        payment_colors = {
            'Cash': self.colors['first'],
            'Credit card': self.colors['second'],
            'Ewallet': self.colors['third']
        }

        grouped_data['color'] = grouped_data['Payment method'].map(payment_colors)

        fig = px.bar(grouped_data, x='Product line', y='Revenue', color='Payment method',
                     color_discrete_map=payment_colors,
                     barmode='group', title='Total Sales by Product Line')
        fig.update_layout(
            height=self.size['height'],
            width=self.size['width'],
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            yaxis=dict(range=[0, 18000]),
            legend=dict(
                x=1,  # Position legend to the right
                y=1.2,  # Position legend at the top
                xanchor='right',  # Anchor the legend to the right side
                yanchor='top',  # Anchor the legend to the top
                title=dict(
                    text=''  # Remove the legend title
                )
            ),
            title=dict(
                text='Total Sales by Product Line',
                font=dict(
                    size=14
                )
            ),
        )
        return fig

    def plot_bar_chart_3(self, df_current_month):
        avg_rating_per_city = df_current_month.groupby(['TimeOfDay', 'City'])['Rating'].mean().reset_index()

        color_map = {
            'Yangon': self.colors['first'],
            'Naypyitaw': self.colors['second'],
            'Mandalay': self.colors['third']
        }

        fig = px.bar(avg_rating_per_city, x='TimeOfDay', y='Rating', color='City', barmode='stack',
                     title='Average Rating per City', text='Rating',
                     color_discrete_map=color_map)

        fig.update_traces(texttemplate='%{text:.2f}', textposition='inside')
        fig.update_layout(
            height=self.size['height'],
            width=self.size['width'],
            xaxis=dict(
                title='Time of Day'  # Set the x-axis title text
            ),
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            yaxis=dict(range=[0, 35]),  # Increase the y-axis range to 40
            bargap=0.4,  # Increase the gap between bars to decrease bar width
            legend=dict(
                x=0.95,  # Position legend further to the right to avoid overlap
                y=1.2,  # Position legend at the top
                xanchor='right',  # Anchor the legend to the left side
                yanchor='top',  # Anchor the legend to the top
                title=dict(
                    text=''  # Remove the legend title
                )
            ),
            title=dict(
                text='Average Rating per City',
                font=dict(
                    size=14
                )
            ),
        )

        return fig

    def plot_line_chart_1(self, df_current_month, df_previous_month):
        daily_revenue_current = df_current_month.groupby('Day')['Revenue'].sum().reset_index()
        daily_revenue_previous = df_previous_month.groupby('Day')['Revenue'].sum().reset_index()

        daily_revenue_current['Month'] = 'Current Month'
        daily_revenue_previous['Month'] = 'Previous Month'

        combined_revenue = pd.concat([daily_revenue_current, daily_revenue_previous])

        fig = px.line(combined_revenue,
                      x='Day',
                      y='Revenue',
                      color='Month',
                      title='Daily Sales',
                      color_discrete_map={'Current Month': self.colors['first'],
                                          'Previous Month': self.colors['second']})
        fig.update_layout(
            height=self.size['height'],
            width=self.size['width'],
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            yaxis=dict(
                tickformat=",",
                title='Revenue',
                rangemode='tozero'
            ),
            legend=dict(
                x=1,
                y=1,
                xanchor='right',
                yanchor='top',  # Anchor the legend to the top
                title=dict(
                    text=''  # Remove the legend title
                )
            ),
            title=dict(
                text='Daily Sales',
                font=dict(
                    size=14
                )
            ),
        )
        # fig.update_yaxes(range=[0, 000], dtick=3000)
        y_tickvals = [-3000, 0, 2000, 4000, 6000, 8000, 10000]
        y_ticktext = ['', '0', '2000', '4000', '6000', '8000', '10000']

        fig.update_yaxes(range=[-2000, 10000], tickvals=y_tickvals, ticktext=y_ticktext)
        return fig

    def plot_line_chart_2(self, df_current_month, df_previous_month):
        daily_quantity_current = df_current_month.groupby('Day')['Quantity'].sum().reset_index()
        daily_quantity_previous = df_previous_month.groupby('Day')['Quantity'].sum().reset_index()

        daily_quantity_current['Month'] = 'Current Month'
        daily_quantity_previous['Month'] = 'Previous Month'

        combined_quantity = pd.concat([daily_quantity_current, daily_quantity_previous])

        fig = px.line(combined_quantity,
                      x='Day',
                      y='Quantity',
                      color='Month',
                      title='Quantities Sold',
                      color_discrete_map={'Current Month': self.colors['first'],
                                          'Previous Month': self.colors['third']})

        fig.update_layout(
            height=self.size['height'],
            width=self.size['width'],
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            legend=dict(
                x=0.99,
                y=1.1,
                xanchor='right',
                yanchor='top',
                traceorder='normal',
                font=dict(
                    size=12,
                ),
                bgcolor='rgba(0,0,0,0)',
                title=dict(
                    text=''  # Remove the legend title
                )
            ),
            title=dict(
                text='Quantities Sold',
                font=dict(
                    size=14
                )
            ),
        )

        # Define tick values and labels for the y-axis
        y_tickvals = [-200, -150, -100, -50, 0, 50, 100, 150, 200, 250, 300, 350, 400]
        y_ticktext = ['', '', '', '', '', '50', '', '150', '', '250', '', '350', '']

        fig.update_yaxes(range=[-200, 400], tickvals=y_tickvals, ticktext=y_ticktext)
        return fig

    def plot_line_chart_3(self, df_current_month):
        grouped_data = df_current_month.groupby(['Day', 'Customer type']).size().reset_index(name='Visits')

        fig = px.line(
            grouped_data,
            x='Day',
            y='Visits',
            color='Customer type',
            title='Daily Visits by Customer Type',
            color_discrete_map={'Member': self.colors['first'], 'Normal': self.colors['third']}
        )

        fig.update_layout(
            height=self.size['height'],
            width=self.size['width'],
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            legend=dict(
                x=0.99,
                y=1.1,
                xanchor='right',
                yanchor='top',
                traceorder='normal',
                font=dict(
                    size=12,
                ),
                bgcolor='rgba(0,0,0,0)',
                title=dict(
                    text=''  # Remove the legend title
                )
            ),
            title=dict(
                text='Daily Visits by Customer Type',
                font=dict(
                    size=14
                )
            ),
        )

        # fig.update_yaxes(range=[-10, 30], dtick=10, tickvals=[0, 10, 20, 30])
        y_tickvals = [-10, -5, 0, 5, 10, 15, 20, 25, 30]
        y_ticktext = ['', '', '', '5', '10', '15', '20', '25', '30']
        fig.update_yaxes(range=[-10, 30], tickvals=y_tickvals, ticktext=y_ticktext)
        return fig

    def plot_bubble_chart_1(self, df_current_month):
        daily_summary_current = df_current_month.groupby(['Day', 'City']).agg(
            {'Quantity': 'sum', 'Revenue': 'sum'}).reset_index()

        fig = px.scatter(daily_summary_current, x='Day', y='Quantity', size='Revenue', color='City',
                         hover_name='City', size_max=17,
                         title='Quantity Sold by city',
                         color_discrete_map={'Mandalay': self.colors['third'], 'Naypyitaw': self.colors['second'],
                                             'Yangon': self.colors['first']}
                         )

        fig.update_layout(
            height=self.size['height'],
            width=self.size['width'],
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            legend=dict(
                x=0.95,  # Position legend to the right
                y=1.2,  # Position legend at the top
                xanchor='right',  # Anchor the legend to the right side
                yanchor='top',  # Anchor the legend to the top side
                title=dict(
                    text=''  # Remove the legend title
                )
            ),
            title=dict(
                text='Quantity Sold by city',
                font=dict(
                    size=14
                )
            ),
        )
        fig.update_yaxes(range=[0, 65])
        return fig

    def show(self):
        st.set_page_config(
            layout="wide",
            page_title="Walmart Sales Dashboard",
            page_icon="assets/walmart_logo.png",
            initial_sidebar_state="collapsed"
        )
        st.sidebar.header('Select a month')
        option = st.sidebar.selectbox(
            ' ',
            ('March', 'February')
        )

        st.subheader(f'{option}')

        if option == 'March':
            df_current_month = self.df_march
            df_previous_month = self.df_february
        elif option == 'February':
            df_current_month = self.df_february
            df_previous_month = self.df_january

        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                bar_chart_1 = self.plot_bar_chart_1(df_current_month)
                st.plotly_chart(bar_chart_1, use_container_width=True, config={'displayModeBar': False})
            with col2:
                bubble_chart_1 = self.plot_bubble_chart_1(df_current_month)
                st.plotly_chart(bubble_chart_1, use_container_width=True, config={'displayModeBar': False})

            with col3:
                line_chart_2 = self.plot_line_chart_2(df_current_month, df_previous_month)
                st.plotly_chart(line_chart_2, use_container_width=True, config={'displayModeBar': False})

        with st.container():
            col4, col5, col6 = st.columns(3)

            with col4:
                bar_chart_2 = self.plot_bar_chart_2(df_current_month)
                st.plotly_chart(bar_chart_2, use_container_width=True, config={'displayModeBar': False})

            with col5:
                bar_chart_3 = self.plot_bar_chart_3(df_current_month)
                st.plotly_chart(bar_chart_3, use_container_width=True, config={'displayModeBar': False})

            with col6:
                line_chart_3 = self.plot_line_chart_3(df_current_month)
                st.plotly_chart(line_chart_3, use_container_width=True, config={'displayModeBar': False})

                # line_chart_1 = self.plot_line_chart_1(self.df_current_month, self.df_previous_month)
                # st.plotly_chart(line_chart_1, use_container_width=True, config={'displayModeBar': False})


if __name__ == '__main__':
    dashboard = Dashboard('dataset/WalmartSalesData.csv')
    dashboard.show()

    styles = f"""
    <style>
    header {{
        visibility: hidden;
    }}

    .block-container.st-emotion-cache-1jicfl2.ea3mdgi5 {{
        padding-bottom: 0px;
        padding-top: 20px;
        padding-right: 25px;
        padding-left: 30px;
    }}

    #walmart-sales-dashboard-march, #walmart-sales-dashboard-february {{
        padding-top: 0px;
        padding-left: 40px;
        font-size:22px;
        padding-bottom:13px;
        color: #ef892c;
    }}

    #march, #february {{
        padding-top: 0px;
        padding-left: 40px;
        font-size:22px;
        padding-bottom:13px;
        color: {Dashboard.colors['third']};
    }}


    div[data-testid="stVerticalBlock"] {{
        gap: 0rem;
    }}

    .viewerBadge_container__r5tak.styles_viewerBadge__CvC9N {{
        z-index: -1;
    }}

    .viewerBadge_link__qRIco {{
        zindex: -1
    }}

    </style>
    """

    st.markdown(styles, unsafe_allow_html=True)
