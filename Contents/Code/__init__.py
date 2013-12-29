# Copyright: Dariush Forouher, 2013

import re, time, datetime, os

class vdr(Agent.Movies):
	name = 'VDR Recordings Importer'
	primary_provider = True
	languages = [Locale.Language.NoLanguage]
	accepts_from = ['com.plexapp.agents.localmedia']

	def search(self, results, media, lang):

	    video_path = String.Unquote(media.filename)
	    folder_path = os.path.dirname(video_path)
	
    	    info_file = Core.storage.load(folder_path+"/info")

    	    title = re.search('^T (.*)$', info_file,re.M)
	    if title:
    		media.name = title.groups(1)[0]

    	    rectime = re.search('^E \d+ (\S*) .*$', info_file,re.M)
	    if rectime:
		media.year = datetime.datetime.fromtimestamp(int(rectime.groups(1)[0])).year

	    results.Append(MetadataSearchResult(id=media.id, year=media.year, name=media.name, lang=Locale.Language.NoLanguage, score=100))

	def update(self, metadata, media, lang):

	    if media is not None and len(media.items)>0 and len(media.items[0].parts)>0:

                video_path = media.items[0].parts[0].file
                folder_path = os.path.dirname(video_path)

		info_file = Core.storage.load(folder_path+"/info")
    
    		channel = re.search('^C \S* (.*)$', info_file,re.M)
		if channel:
    		    metadata.studio = channel.groups(1)[0]

    		rectime = re.search('^E \d+ (\S*) .*$', info_file,re.M)
		if rectime:
        	    metadata.originally_available_at = datetime.datetime.fromtimestamp(int(rectime.groups(1)[0]))
		    metadata.year = metadata.originally_available_at.year

    		title = re.search('^T (.*)$', info_file,re.M)
		if title:
        	    metadata.title = title.groups(1)[0]

    		tagline = re.search('^S (.*)$', info_file,re.M)
		if tagline:
        	    metadata.tagline = tagline.groups(1)[0]

    		summary = re.search('^D (.*)$', info_file,re.M)
		if summary:
        	    metadata.summary = summary.groups(1)[0]

		# TODO: genres are encoded. too lazy to write lookup table for table 28 of
		# http://www.etsi.org/deliver/etsi_en/300400_300499/300468/01.12.01_40/en_300468v011201o.pdf
    		# genre = re.search('^G (.*)$', info_file,re.M)
		# if genre:
		#     metadata.genres.clear()
        	#     metadata.genres.add(genre.groups(1)[0])

		# never observed this, not sure about semantics
    		# rating = re.search('^R (.*)$', info_file,re.M)
		# if rating:
        	#     metadata.rating = rating.groups(1)[0]

		return metadata
