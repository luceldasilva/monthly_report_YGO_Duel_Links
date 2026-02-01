# install.packages("here")
# install.packages("glue")
# install.packages("calendR")
# install.packages("styler")

library(glue)
library(here)
library(calendR)


base_path <- here("etl", "output")
date_file <- here(base_path, "date_df.rds")
summary_file <- here(base_path, "summary_df.rds")

summary_df <- readRDS(summary_file)
date_df <- readRDS(date_file)

kc_cup <- summary_df$kc_cup[1]
year <- summary_df$year[1]
month <- summary_df$monthy[1]

now <- Sys.time()
today <- format(now, "%d_%m_%Y_%H_%M_%S")

calendar_photo <- here(base_path, glue("calendar_{year}_{month}_{today}.png"))


if (kc_cup) {
  url_image <- 'https://monthly-report-yugioh-dl.vercel.app/reports/plantilla/calendr/para_kc_cup.png'

  days <- rep(0, summary_df$n_days[1])

  first_day <- summary_df$first_day[1]
  last_day <- summary_df$last_day[1]

  date_df <- date_df[date_df$day_of_monthy >= first_day & date_df$day_of_monthy <= last_day, ]

  days[first_day:last_day] <- date_df$jugadores
} else {
  url_image <- 'https://monthly-report-yugioh-dl.vercel.app/reports/plantilla/calendr/para_kog.png'
  days <- date_df$jugadores
}


png(calendar_photo, width = 1000, height = 800, res = 150)
calendR(
  year = year,
  month = month,
  special.days = days,
  gradient = TRUE,
  low.col = "white",
  special.col = "#03edfdff",
  legend.pos = "bottom",
  legend.title = "Registros",
  text = as.character(date_df$jugadores),
  text.pos = date_df$day_of_month,
  bg.img = url_image
)
dev.off()


file.remove(date_file)
file.remove(summary_file)