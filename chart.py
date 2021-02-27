import plotly.express as px
import pandas as pd
import os
# import plotly.graph_objects as go

def create_figure(info_dict, file_name):
    if not os.path.exists("static"):
        os.mkdir("static")
    path = "static/%s" % file_name
    keys = info_dict.keys()
    values = info_dict.values()
    df = pd.DataFrame(dict(
        r=values,
        theta=keys
    ))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True, template="plotly_dark")
    fig.update_traces(fill='toself')
    #fig.show()
    fig.write_image(path)
    return 0
    # using plotly graph objects
    # keys = list(info_dict.keys())
    # values = list(info_dict.values())
    # fig = go.Figure(data=go.Scatterpolar(r=values, theta=keys, fill='toself'))
    # fig.update_layout(
    #     polar=dict(
    #         radialaxis=dict(
    #             visible=True,
    #             range=[0, 1]
    #         )),
    #     showlegend=False
    # )
    # fig.show()


if __name__ == "__main__":
    test_dict = {
        'sadness': 0.368929,
        'joy': 0.33916,
        'fear': 0.351127,
        'disgust': 0.036447,
        'anger': 0.041098
    }
    file_name = "testing_file.jpeg"
    create_figure(test_dict, file_name)
