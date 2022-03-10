library(tidyverse)
library(ggplot2)
library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(dashBootstrapComponents)
library(plotly)

data <- read.csv('https://github.com/ubco-mds-2021-labs/dashboard1-group-g/raw/main/data/clean_spotify.csv', sep = '\t')

count_vs_year <- function(data){
  plot <- ggplot(data, aes(x = Year, color = Playlist.Genre)) + 
    geom_line(stat = 'count') + 
    theme_classic() + 
    labs(x = "Album Release Year", y = "Number of Songs Released", color = "Genre")
}


app <- Dash$new(external_stylesheets = dbcThemes$BOOTSTRAP)

app$layout(
  dbcContainer(
    list(
      dccGraph(id = "timecountplot"),
      dccDropdown(
        id = "genre-widget",
        options = list(list(label = "Pop", value = "Pop"),
                       list(label = "Rap", value = "Rap"),
                       list(label = "Rock", value = "Rock"),
                       list(label = "Latin", value = "Latin"),
                       list(label = "R&B", value = "R&B"),
                       list(label = "Edm", value = "Edm")
                       ),
        value = unique(df$Playlist.Genre), 
        multi = TRUE
      )
    )
  )
)

app$callback(
  output('timecountplot', 'figure'),
  list(input('genre-widget', 'value')),
  function(genres) {
    print(genres)
    newData <- data |> filter(Playlist.Genre %in% genres)
    p <- count_vs_year(newData)
    ggplotly(p)
  }
)

app$run_server(debug = T)