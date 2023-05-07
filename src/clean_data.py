import re
import pandas as pd
import glob

def clean_lyric(my_string):
    my_new_string = re.sub('''[/[!.,?/'/"]''',"",my_string).replace('''\\n''','').lower()
    return(my_new_string)

def read_any(folder):
    any = glob.glob(f"{folder}/*")
    return(any)

def clean_all_lyrics(local_lyrics, local_save):
    all_lyrics = read_any(local_lyrics)
    df = pd.DataFrame({'song': [],
                   'artist': [],
                   'views': [],
                   'n_verses': [],
                   'n_rows': [],
                   'lyric': [],
                   'clean_lyric': []})

    for lyric in all_lyrics[:1000]:

        try:
            lyric_df = pd.read_table(lyric, 
                        header=None)
        except:
            print("Error reading the file!")
        
        df_aux = pd.DataFrame({'song': [lyric_df[0][0].replace('Song:', '')],
                    'genre': [lyric.split('\\')[-1].split('___')[0]],
                    'directory': [lyric],
                    'artist': [lyric_df[0][1].replace('Artist:', '')],
                    'views': [lyric_df[0][2].replace('Views:', '')],
                    'n_verses': [lyric_df[0][3].replace('Verses:', '')],
                    'n_rows': [len(lyric_df[0][4].split('''','''))],
                    'lyric': [lyric_df[0][4]],
                    'clean_lyric': [clean_lyric(lyric_df[0][4])]})
        
        df = pd.concat([df, df_aux])

    df = df.reset_index()
    df.to_csv(f'{local_save}/silver_data_lyrics.csv',index=False)