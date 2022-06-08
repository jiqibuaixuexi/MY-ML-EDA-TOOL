import os
# 把版本降到0.84.0，否则df.dtypes会报错
import streamlit as st

# EDA Pkgs
import pandas as pd

# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

def main():
    """
    Common ML Dataset Explorer
    """
    st.title("Common ML Dataset Explorer")
    st.subheader("Simple Data Science Explorer with Streamlit")
    # 设置下面markdown的文本框颜色和字体大小
    html_temp = """
    <div style="background-color:tomato;"><p style="color:white;font-size:50px">Streamlit is Awesome</p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    def file_selector(folder_path=r'.\dataset'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("Select A file",filenames)
        return os.path.join(folder_path,selected_filename)

    filename = file_selector()
    st.info("You Selected {}".format(filename))

    # Read Data
    df = pd.read_csv(filename)
    # Show Dataset
    if st.checkbox("Show Dataset"):
        number = st.number_input("Number of Rows to View",5,20) #想看前几行
        st.dataframe(df.head(number))
    # Show Columns
    if st.button("Column Names"):
        st.write(df.columns)

    # Show Shape
    if st.checkbox("Shape of Dataset"):
        st.write(df.shape)
        data_dim = st.radio("Show Dimension By",("Rows","Columns"))
        if data_dim =="Rows":
            st.text("Number of Rows")
            st.write(df.shape[0])
        elif data_dim =="Columns":
            st.text("Number of Cloumns")
            st.write(df.shape[1])      
            
    # Select Columns
    if st.checkbox("Select Columns To Show"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select",all_columns)
        new_df = df[selected_columns]
        st.dataframe(new_df)
    # Show Values
    if st.button("Value Counts"):
        st.text("Value Counts By Target/Class")
        st.write(df.iloc[:,-1].value_counts()) # 每个类别变量的个数

    # Show Datatypes
    if st.button("Show Datatypes"):    
        st.write(df.dtypes) 

    # Show Summary
    if st.checkbox("Summary"):
        st.write(df.describe().T)


    ## Plot and Visualization

    st.subheader("Data Visualization")
    # Correlation #TODO

    # Seaborn Plot
    if st.checkbox("Correlation Plot[Seaborn]"):
        st.write(sns.heatmap(df.corr(),annot=True))
        st.pyplot()

    # Count Plot #TODO
    if st.checkbox("Plot of Value Counts"):
        st.text("Value Counts By Target")
        all_columns_names = df.columns.tolist()
        primary_col = st.selectbox("Primary Column to GroupBy",all_columns_names)
        selected_columns_names = st.multiselect("Select Columns",all_columns_names)
        if st.button("Plot"):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].count()
            else:
                vc_plot = df.iloc[:,-1].valuecounts()
            st.write(vc_plot.plot(kind="bar"))
            st.pyplot()

    # Pie Chart
    if st.checkbox("Pie Plot"):
        all_columns_names = df.columns.tolist()
        if st.button("Generate Pie Plot"):
            st.success("Generating A Pie Plot")
            st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
            st.pyplot()

    # Customizable Plot

    st.subheader("Customizable Plot")
    all_columns_names = df.columns.tolist()
    type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
    selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)

    if st.button("Generate Plot"):
        st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

        # Plot By Streamlit
        if type_of_plot=="area":
            cust_data = df[selected_columns_names]
            st.area_chart(cust_data)

        elif type_of_plot=="bar":
            cust_data = df[selected_columns_names]
            st.bar_chart(cust_data)

        elif type_of_plot=="line":
            cust_data = df[selected_columns_names]
            st.line_chart(cust_data)  
     

        # Custom Plot
        elif type_of_plot=="box":
            cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
            st.write(cust_plot)
            st.pyplot()


        # TODO
        # "hist","kde","Correlation"

    if st.button("Thankes"):
            st.balloons()



if __name__=="__main__":
    main()

