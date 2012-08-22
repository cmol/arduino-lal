#!/usr/bin/env python
import sqlite3
from xml.dom.minidom import Document

doc = Document()
wml = doc.createElement('wml')

db = sqlite3.connect('log.db')
db.row_factory = sqlite3.Row
c = db.cursor()

columns = ['wind_direction', 'wind_speed', 'temperature', 'preasure', 'humidity']
columns_sql = []
for column in columns:
  columns_sql.append('min({0}) as min_{0}, max({0}) as max_{0}, avg({0}) as avg_{0}'.format(column))


c.execute('SELECT count(logged) as samples, strftime("%Y-%m-%d %H:%M", logged) as logged, {0} FROM log GROUP BY logged'.format(','.join(columns_sql)))
rows = c.fetchall()


types = ['avg', 'min', 'max']

for row in rows:
  logEntry = doc.createElement('logEntry')

  column_node = doc.createElement('logged')
  text_node = doc.createTextNode(str(row['logged']))
  column_node.appendChild(text_node)
  logEntry.appendChild(column_node)

  column_node = doc.createElement('duration')
  text_node = doc.createTextNode('1 minute')
  column_node.appendChild(text_node)
  logEntry.appendChild(column_node)

  column_node = doc.createElement('samples')
  text_node = doc.createTextNode(str(row['samples']))
  column_node.appendChild(text_node)
  logEntry.appendChild(column_node)

  for column in columns:
    for datatype in types:
      column_node = doc.createElement('{0}_{1}'.format(datatype, column))
      text_node = doc.createTextNode(str(row['{0}_{1}'.format(datatype, column)]))
      column_node.appendChild(text_node)
      logEntry.appendChild(column_node)

  wml.appendChild(logEntry)

doc.appendChild(wml)
print doc.toprettyxml()
