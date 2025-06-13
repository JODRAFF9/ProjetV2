import streamlit as st
import plotly.express as px
from funcs import map

def analyse(data):
    map(data)
    col1, col2,col3= st.columns(3)


    with col1:
        st.markdown(
            f"""
            <div style="max-width: 320px;margin: 30px auto;
                background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
                color: #222;
                border-radius: 16px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                padding: 32px 24px 24px 24px;
                text-align: center;
                font-family: 'Segoe UI', Arial, sans-serif;">
                <div style="font-size: 38px; margin-bottom: 10px;">👥</div>
                <div style="font-size: 22px; font-weight: 600; color: #007acc; margin-bottom: 6px;">
                    Nombre de clients
                </div>
                <div style="font-size: 40px; font-weight: bold; color: #01579b;">
                    { data.shape[0] }
                    </div> 
            </div>            
            
            
            """,
            unsafe_allow_html=True
        )

    with col2:
        churn_rate = (data['Exited'] == "Yes").mean() * 100
        st.markdown(
            f"""
            <div style="max-width: 320px;margin: 30px auto;
                background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
                color: #222;
                border-radius: 16px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                padding: 32px 24px 24px 24px;
                text-align: center;
                font-family: 'Segoe UI', Arial, sans-serif;">
                <div style="font-size: 38px; margin-bottom: 10px;">❌</div>
                <div style="font-size: 22px; font-weight: 600; color: #007acc; margin-bottom: 6px;">
                    Nombre de clients
                </div>
                <div style="font-size: 40px; font-weight: bold; color: #01579b;">
                    {churn_rate:.2f}
                    </div> 
            </div>                   
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")
    
    with col3:
        avg_salary = data["EstimatedSalary"].mean()
        st.markdown(
            f"""
            <div style="max-width: 320px;margin: 30px auto;
                background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
                color: #222;
                border-radius: 16px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                padding: 32px 24px 24px 24px;
                text-align: center;
                font-family: 'Segoe UI', Arial, sans-serif;">
                <div style="font-size: 38px; margin-bottom: 10px;">💰 </div>
                <div style="font-size: 22px; font-weight: 600; color: #007acc; margin-bottom: 6px;">
                    Le salaire moyen
                </div>
                <div style="font-size: 40px; font-weight: bold; color: #01579b;">
                    {avg_salary}
                    </div> 
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
    
    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(fig1, use_container_width=True)
    with col6:
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🎯 la relation entre âge et Churn")
    st.plotly_chart(fig3, use_container_width=True)
 