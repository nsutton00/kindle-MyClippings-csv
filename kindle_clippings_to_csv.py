import pandas
import sys

#Util functions
def format_author(author_str):
  '''
  Author in clippings is in format: LastName, First Name
  Take author name and return it as FirstName LastName
  '''
  author = author_str.replace(',','').split(' ') 
  return ' '.join(reversed(author))

#Main function
def main(f_path):
  clippings_txt = open(f_path, 'r', encoding='utf-8').read()
  clippings_list = clippings_txt.split('==========')

  output = []

  for highlight in clippings_list:
    parts = highlight.split('\n')
    
    try:
      title = parts[1].split('(')[0].strip()
      author = format_author(parts[1][parts[1].find("(")+1:parts[0].find(")")])
      text = parts[4]

      #If page can not be accessed, leave blank and continue with highlight
      try:
        page = parts[2].split('- Your Highlight on page ')[1].split('|')[0].strip()
      except:
        page = ''

    except IndexError:
      #Skips any malformed highlights
      print(f'{parts} - Index error, skipping line...')
      pass
    
    highlight_df = pandas.DataFrame({
      'title': title,
      'author': author,
      'page': page,
      'text': text,
    }, index=[0])
    output.append(highlight_df)

  output_df = pandas.concat(output, ignore_index=True)
  output_df.dropna()

  output_df.to_csv('KindleHighlights.csv', encoding='utf-8-sig')
  print('Highlights CSV has been saved to the directory of this script.')

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print('Please provide the path to your My Clippings.txt file as a positional arguement in quotes:', '--> kindle_extract_clippings_to_csv.py "/path_to_My Clippings.txt"', sep='\n')
  else:
    main(sys.argv[1])