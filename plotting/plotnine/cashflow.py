import matplotlib.pyplot as plt
import numpy as np
import plotnine as p9
import pandas as pd

# Set the figure size of plotnine
p9.options.figure_size = (8, 4)

cashflow_years = np.arange(2024, 2028, 1).tolist()

# Create a dataframe
cashflowOneYear = pd.DataFrame(
    {
        "Year": cashflow_years,
        "Type": ["one-year"] * len(cashflow_years),
        "Cashflow": [35] + [0] * (len(cashflow_years)-1),
    }
)

cashflowMultiYear = pd.DataFrame(
    {
        "Year": cashflow_years,
        "Type": ["multi-year"] * len(cashflow_years),
        "Cashflow": [35, 34, 33, 31],
    }
)

cashflow = pd.concat([cashflowOneYear, cashflowMultiYear])
cashflow.Type = pd.Categorical(cashflow.Type, categories=cashflow.Type.unique(), ordered=True)  

def plot_cashflow(cashflow: pd.DataFrame, highlight_year: int, title:str = "", show: bool =True) -> None:
    
    # Create a plot using plotnine
    cashflow_plot = (
        p9.ggplot(cashflow, p9.aes(x="Year", y="Cashflow"))
        # + p9.geom_col(fill="#3C4150")
        + p9.geom_bar(
            fill=np.where(cashflow["Year"] == highlight_year, "#418CE1", "#A1B1AD"),
            stat="identity",  #  position="identity"
            width=.3,
        )
        + p9.facet_grid("Type~")  # , scales="free_y"
        # + p9.facet_wrap("Type", nrow=2)  # , scales="free_y"
        + p9.geom_text(p9.aes(label="Cashflow"), nudge_y=3, size=10)
        + p9.labs(title=title, x="Year", y="Premium")
        + p9.theme_minimal()
        # + p9.theme_void()
        # + p9.theme_538()
        + p9.theme(
            text=p9.element_text(family="DejaVu Sans", size=10),
            axis_title=p9.element_text(face="bold"),
            axis_text=p9.element_text(face="italic"),
            plot_title=p9.element_text(face="", size=12, hjust = 0.5),
            strip_text_y=p9.element_text(angle=-90, ), # orientation facet lables
            # axis_title_y=p9.element_blank(),
            # axis_text_y=p9.element_blank(),
        )
    )
    # Show the plot
    return cashflow_plot.draw(show=show)


# TODO:
# put labels inside the bars
# use Swiss Re color palette: #1455B4 #418CE1 #91C8FF #A1B1AD #3C4150 (see below or email from Shashank Malhotra)
# no background lines and now y-labels
# add arrows to x-axis: https://stackoverflow.com/questions/33737736/matplotlib-axis-arrow-tip

    
fig = plot_cashflow(cashflow, highlight_year=2024)
# , title='Premium cash flows for Marx 4 (2024M01)'

# plt.show()



# Annotate each category using geom_text
# (
#     p9.ggplot(data=medal_noc_count)
#     + p9.geom_bar(
#         p9.aes(x="NOC", y="Count"),
#         fill=np.where(medal_noc_count["NOC"] == "URS", "#c22d6d", "#80797c"),
#         stat="identity",
#     )
#     + p9.geom_text(p9.aes(x="NOC", y="Count", label="Count"), size=10, nudge_y=0.5)
#     + p9.labs(title="Top ten countries that won the most Olympic medals")
#     + p9.xlab("Country")
#     + p9.ylab("Frequency")
#     + p9.scale_x_discrete(limits=medal_noc_count["NOC"].tolist())
#     + p9.theme_minimal()
#     + p9.theme(
#         text=p9.element_text(family="DejaVu Sans", size=10),
#         axis_title=p9.element_text(face="bold"),
#         axis_text=p9.element_text(face="italic"),
#         plot_title=p9.element_text(face="bold", size=12),
#     )
# )



# my_custom_theme = p9.theme(axis_text_x = p9.element_text(color="grey", size=10,
#                                                          angle=90, hjust=.5),
#                            axis_text_y = p9.element_text(color="grey", size=10))
# (p9.ggplot(data=survey_202X,
#            mapping=p9.aes(x='factor(year)'))
#     + p9.geom_bar()
#     + my_custom_theme
# )


# # Swiss Re Blue color codes:
# color_codes = ["#3C4150", "#A1B1AD" "#91C8FF", "#418CE1" "#1455B4"]
# color_keys = df.Delivery.unique().tolist()
# colors = dict(zip(color_keys, color_codes[0 : len(color_keys)]))
# gg = gg +  p9.scales.scale_color_manual(values=colors)
