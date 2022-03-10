library(dash)
library(dashHtmlComponents)
library(tidyverse)
library(ggplot2)
library(plotly)

#Create the app
app <- dash_app()

#header
tophead <- div(
    dbcRow(
        list(
            dbcCol(
                div("Spotified"),
                width = 6,
                style = list("color" = "green", "background-color" = "black", "textAlign" = "center", "height" = 40), # nolint
                md = 6 # nolint
            ),
            dbcCol(
                img(
                    src = "data/assets/logo1.png"
                )
            )
        )
    )
)




























# tophead <- htmlDiv(list(

#         htmlDiv(list(), className = 'col-2'), #Same as img width, allowing to have the title centrally aligned # nolint

#         htmlDiv(list(
#             htmlH1('Spotified', # nolints
#                     style = list('textAlign' = 'center', 'color' = 'green') # nolint
#             )),
#             className = "col-8"
#         ),

#         htmlDiv(list(
#             htmlImg(
#                     src = "logo1.png",
#                     height = "50 px",
#                     width = "auto")
#             ),
#             className = "col-1",
#             style = list(
#                     "align-items" = "center",
#                     "padding-top" = "2%",
#                     "height" = "auto"))

#         ),
#         className = "row",
#         style = list("height" = "4%",
#                 "background-color" = "Black")
#         )

dropdown <- htmlDiv(
                list(
                    htmlH3('Genre', # nolint
                    style = list('color' = 'black', 'background-color'='green')) # nolint
                )
)

dp <- htmlDiv(list(dbcRow(list(htmlDiv(list(
            htmlH3(children = "Genre",
                    style = list("textAlign" = "start", "color" = "black")
            )),
            className = "col-2"
        ),
            htmlDiv(list(dccDropdown(
                options = list(list(label = "New York City", value = "NYC"),
                value = "NYC",
                id = "genre_widget")
            ), className = "col-5",
                     style = list("height" = "2%",
                "background-color" = "black", "align-items" = "end")
            )
        ))
),
        className = "row",
        style = list("height" = "2%", # nolint
                "background-color" = "green"))
)

#Layout
app %>% set_layout(tophead, dp)

#To run the app
app %>% run_app()