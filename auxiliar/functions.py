import dataframe_image as dfi

# Function that saves a df as an image
def saves_png(df, img_name, path):
	dfi.export(df, f'{path}{img_name}.png', table_conversion='matplotlib')