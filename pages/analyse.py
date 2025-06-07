import streamlit as st
import plotly.express as px

def analyse1(data):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#f0f8ff;color:black; padding:10px; border-radius:10px; text-align:center">
                <h3>👥 Clients</h3>
                <p style="font-size:25px; color:#007acc;"><strong>{data.shape[0]}</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        churn_rate = (data['Exited'] == "Yes").mean() * 100
        st.markdown(
            f"""
            <div style="background-color:#fff0f0;color:black; padding:10px; border-radius:10px; text-align:center">
                <h3>❌ Churn Rate</h3>
                <p style="font-size:25px; color:#cc0000;"><strong>{churn_rate:.2f} %</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        avg_salary = data["EstimatedSalary"].mean()
        st.markdown(
            f"""
            <div style="background-color:#f0fff0;color:black; padding:10px; border-radius:10px; text-align:center">
                <h3>💰 Salaire Moyen</h3>
                <p style="font-size:25px; color:#008000;"><strong>{avg_salary:,.0f} €</strong></p>
            </div>
            """,
            unsafe_allow_html=True
    )

    st.markdown("---")
    
    @st.cache_data
    def compute_gender_churn(df):
        return df.groupby(['Gender', 'Exited']).size().reset_index(name='count')

    @st.cache_data
    def compute_figs(df):
        fig1 = px.histogram(df, x="Geography", color="Exited", barmode="group",
                            title="Churn par Géographie", color_discrete_map={"No": "green", "Yes": "red"})
        fig1.update_layout(transition=dict(duration=0))

        gender_churn = compute_gender_churn(df)
        fig2 = px.bar(gender_churn, x='Gender', y='count', color='Exited',
                    title="Churn par Sexe", barmode="group",
                    color_discrete_map={"No": "green", "Yes": "red"})
        fig2.update_layout(transition=dict(duration=0))

        fig3 = px.box(df, x='Exited', y='Age', color='Exited',
                    title='Âge selon Churn', color_discrete_map={"No": "green", "Yes": "red"})
        fig3.update_layout(transition=dict(duration=0))

        return fig1, fig2, fig3
    
    fig1, fig2, fig3 = compute_figs(data)
    
    col4, col5 = st.columns(2)
    with col4:
        st.plotly_chart(fig1, use_container_width=True)
    with col5:
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🎯 la relation entre âge et Churn")
    st.plotly_chart(fig3, use_container_width=True)
 