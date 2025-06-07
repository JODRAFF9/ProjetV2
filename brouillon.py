
    # # 1. Répartition du Churn par Pays
    # col4, col5 = st.columns(2)
    # with col4:
    #     fig1 = px.histogram(train_df_labelled, x="Geography", color="Exited", barmode="group",
    #                         title="Churn par Géographie", color_discrete_map={"No":"green", "Yes":"red"})
    #     st.plotly_chart(fig1, use_container_width=True)

    # # 2. Répartition homme/femme dans le churn
    # with col5:
    #     gender_churn = train_df_labelled.groupby(['Gender', 'Exited']).size().reset_index(name='count')
    #     fig2 = px.bar(gender_churn, x='Gender', y='count', color='Exited',
    #                 title="Churn par Sexe", barmode="group",
    #                 color_discrete_map={"No":"green", "Yes":"red"})
    #     st.plotly_chart(fig2, use_container_width=True)

    # # 3. Age vs Churn
    # st.markdown("### 🎯 la rélation entre âge et Churn")
    # fig3 = px.box(train_df_labelled, x='Exited', y='Age', color='Exited', 
    #             title='Répartition de l\'âge selon le statut (Churn)', 
    #             color_discrete_map={"No": "green", "Yes": "red"})
    # st.plotly_chart(fig3, use_container_width=True)

    # # 4. Corrélation entre variables numériques
    # st.markdown("### 🔍 Corrélation")
    # correlation = train_df_labelled[num_cols].corr()
    # fig4 = px.imshow(correlation, text_auto=True, color_continuous_scale='RdBu_r',
    #                 title="Matrice de Corrélation")
    # st.plotly_chart(fig4, use_container_width=True)

    # # 5. Sélection interactive : Salary vs Churn selon le pays
    # st.markdown("### 📊 Analyse personnalisée")
    # selected_country = st.selectbox("Choisir un pays", train_df_labelled["Geography"].unique())
    # filtered_train_df_labelled = train_df_labelled[train_df_labelled["Geography"] == selected_country]

    # fig5 = px.scatter(filtered_train_df_labelled, x="EstimatedSalary", y="Age", color="Exited",
    #                 title=f"Salaire vs Âge ({selected_country})",
    #                 color_discrete_map={0:"green", 1:"red"})
    # st.plotly_chart(fig5, use_container_width=True)
        
    
    
# """     """
#     if st.checkbox("Afficher les données brutes"):
#         st.dataframe(train_df.head(100))

#     st.write("### Statistiques descriptives")
#     st.write(train_df_labelled[num_cols].describe())

#     st.write("### Visualisation de deux variables")

#     nomx = st.selectbox("Variable X", noms_descriptifs)
#     nomy = st.selectbox("Variable Y", noms_descriptifs)

#     variable_x=nom_variable(nomx,mode="vers_technique")
#     variable_y=nom_variable(nomy,mode="vers_technique")


#     # Visualisation des relations entre les variables
#     fig, ax = plt.subplots(figsize=(10, 8))
#     if variable_x in num_cols and variable_y in num_cols:
#         sns.scatterplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, color="teal", s=100, edgecolor='black')
#         ax.set_title(f"Nuage de points entre {nomx} et {nomy}", fontsize=16, fontweight='bold')
#         ax.set_xlabel(variable_x, fontsize=14)
#         ax.set_ylabel(variable_y, fontsize=14)
#         ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
#         ax.grid(True, linestyle='--', alpha=0.7)
#     elif (variable_x in cat_cols or variable_x in target) and (variable_y in cat_cols or variable_y in target):
#         grouped_train_df_labelled = train_df_labelled.groupby([variable_x, variable_y]).size().unstack()
#         grouped_train_df_labelled.plot(kind='bar', stacked=True, ax=ax, cmap='coolwarm')
#         ax.set_title(f"Graphique en barres empilées de {nomx} par {nomy}", fontsize=16, fontweight='bold')
#         ax.set_xlabel(variable_x, fontsize=14)
#         ax.set_ylabel("Effectifs", fontsize=14)
#         ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
#         ax.legend(title=variable_y, fontsize=12)
#     else:
#         sns.boxplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, palette="Set2")
#         ax.set_title(f"Graphique de boîte de {nomy} par {nomx}", fontsize=16, fontweight='bold')
#         ax.set_xlabel(variable_x, fontsize=14)
#         ax.set_ylabel(variable_y, fontsize=14)
#         ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)

#     st.pyplot(fig)
#     st.write("---")

#     st.write("### Matrice de Corrélation")
#     correlation_matrix = train_df_labelled[num_cols].corr()
#     mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
#     fig_corr, ax_corr = plt.subplots(figsize=(14, 12))
#     sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", mask=mask, fmt=".2f")
#     st.pyplot(fig_corr)*/
#     """ """