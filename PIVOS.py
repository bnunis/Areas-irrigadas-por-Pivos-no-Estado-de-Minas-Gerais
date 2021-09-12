#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd 
import pandas as pd 
import numpy as np 
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.pyplot as plt


# In[2]:


# Lendo o shapefile do estado de Minas Gerais
shapefile = gpd.read_file("C:/Users/breno/Desktop/PIVOS/MUNICIPIOS/ide_1103_mg_municipios_pol.shp")
shapefile = shapefile.sort_values(by=['cidade'], ascending=True)
shapefile.reset_index(inplace=True, drop=True)
shapefile.plot()
shapefile.head()


# In[3]:


#Abrindo a tabela em csv 
tabela = pd.read_csv('C:/Users/breno/Desktop/PIVOS/TABELA.csv', sep=';')

#Transformando os dados de area para float 
tabela["area_ha"] = tabela["area_ha"].str.replace(",", ".")  
tabela["area_ha"] = tabela["area_ha"].astype(float)
tabela.head()


# In[4]:


#Associação das areas por cidade
tabela_nova = tabela.groupby(['cidade'])['area_ha'].sum().reset_index()
tabela_nova = tabela_nova.sort_values(by=['cidade'], ascending=True)
tabela_nova.reset_index(inplace=True, drop=True)
tabela_nova.head()


# In[5]:


# Salvando data frame em CSV 
tabela_nova.to_csv('C:/Users/breno/Desktop/PIVOS/TABELA_NOVA.csv',sep=';', index=False, float_format='%.2f')


# In[6]:


# Unindo os dois Datas Frames com merge do pandas
shapefile_novo = shapefile.merge(tabela_nova, how='left', left_index= True, right_index= True)
shapefile_novo.head()


# In[7]:


# Substitui NaN por 0 
shapefile_novo.replace(np.nan, 0, inplace=True)
shapefile_novo.head()


# In[8]:


# Salvando novo Shapefile
shapefile_novo.to_file(driver='ESRI Shapefile',filename=r'C:/Users/breno/Desktop/PIVOS/MUNICIPIOS/pivos.shp')


# In[9]:


# Plotando mapa com áreas de irrigação por pivô por municipio do estado de Minas Gerais 

shapefile_novo.plot(column='area_ha', cmap='Reds', figsize=(12,10), legend=True, edgecolor='black')
plt.title('Áreas/ha Irrigadas por Pivôs nos Municipios de Minas Gerais/MG',fontdict={'fontsize': '16', 'fontweight': '3'})
scalebar = ScaleBar(20000, units="m",location='lower left')
plt.gca().add_artist(scalebar)

