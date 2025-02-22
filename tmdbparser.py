from tmdbv3api import TMDb, TV, Search
import re
from torcategory import GuessCategoryUtils
from tortitle import parseMovieName
from difflib import SequenceMatcher


def transFromCCFCat(cat):
    if re.match('(Movie)', cat, re.I):
        return 'movie'
    elif re.match('(TV)', cat, re.I):
        return 'tv'
    else:
        return cat


def transToCCFCat(mediatype, originCat):
    if mediatype == 'tv':
        return 'TV'
    elif mediatype == 'movie':
        if not re.match('(movie)', originCat, re.I):
            return 'Movie'
    return originCat


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class TMDbNameParser():
    def __init__(self, tmdb_api_key, tmdb_lang, ccfcat_hard=None):
        self.ccfcatHard = ccfcat_hard
        self.ccfcat = ''
        self.title = ''
        self.year = 0
        self.tmdbid = 0
        self.season = ''
        self.episode = ''
        self.cntitle = ''
        self.resolution = ''
        self.group = ''
        self.tmdbcat = ''
        self.original_language = ''
        self.popularity = 0
        self.poster_path = ''
        self.genre_ids =[]

        if tmdb_api_key:
            self.tmdb = TMDb()
            self.tmdb.api_key = tmdb_api_key
            self.tmdb.language = tmdb_lang
        else:
            self.tmdb = None
            # self.tmdb.api_key = None

    def clearData(self):
        self.ccfcat = ''
        self.title = ''
        self.year = 0
        self.tmdbid = -1
        self.season = ''
        self.episode = ''
        self.cntitle = ''
        self.resolution = ''
        self.group = ''
        self.tmdbcat = ''
        self.original_language = ''
        self.popularity = 0
        self.poster_path = ''
        self.genre_ids =[]

    def parse(self, torname, TMDb=False):
        self.clearData()
        catutil = GuessCategoryUtils()
        self.ccfcat, self.group = catutil.guessByName(torname)
        self.resolution = catutil.resolution
        self.title, parseYear, self.season, self.episode, self.cntitle = parseMovieName(
            torname)

        if self.season and (self.ccfcat != 'TV'):
            # print('Category fixed: ' + movieItem)
            self.ccfcat = 'TV'
        if self.ccfcat == 'TV':
            self.season = self.fixSeasonName(self.season)

        if self.ccfcatHard:
            self.ccfcat = self.ccfcatHard

        self.tmdbcat = transFromCCFCat(self.ccfcat)

        if TMDb:
            if self.tmdbcat in ['tv', 'movie', 'Other', 'HDTV']:
                self.searchTMDb(self.title, self.tmdbcat,
                                parseYear, self.cntitle)
            self.ccfcat = transToCCFCat(self.tmdbcat, self.ccfcat)

    def fixSeasonName(self, seasonStr):
        if re.match(r'^Ep?\d+(-Ep?\d+)?$', seasonStr,
                    flags=re.I) or not seasonStr:
            return 'S01'
        else:
            return seasonStr.upper()

    # def verifyYear(self, resultDate, checkYear, cat):
    #     match = False
    #     resyear = checkYear
    #     m = re.match(r'^(\d+)\b', resultDate)
    #     if m:
    #         resyear = m.group(0)
    #         intyear = int(resyear)
    #         if cat == 'tv':
    #             match = not (self.season == 'S01' and self.year and self.year not in [str(intyear-1), str(intyear), str(intyear+1)])
    #         else:
    #             match = not self.year or (self.year in [str(intyear-1), str(intyear), str(intyear+1)])
    #     if match:
    #         self.year = resyear
    #     return match

    def saveTmdbTVResultMatch(self, result):
        if result:
            if hasattr(result, 'name'):
                self.title = result.name
                # print('name: ' + result.name)
            elif hasattr(result, 'original_name'):
                self.title = result.original_name
                # print('original_name: ' + result.original_name)
            self.tmdbid = result.id
            self.tmdbcat = 'tv'
            if hasattr(result, 'original_language'):
                if result.original_language == 'zh':
                    self.original_language = 'cn'
                else:
                    self.original_language = result.original_language
            if hasattr(result, 'popularity'):
                self.popularity = result.popularity
            if hasattr(result, 'poster_path'):
                self.poster_path = result.poster_path
            if hasattr(result, 'first_air_date'):
                self.year = self.getYear(result.first_air_date)
            elif hasattr(result, 'release_date'):
                self.year = self.getYear(result.release_date)
            else:
                self.year = 0
            if hasattr(result, 'genre_ids'):
                self.genre_ids = result.genre_ids
            print('Found [%d]: %s' % (self.tmdbid, self.title))
        else:
            print('\033[33mNot match in tmdb: [%s]\033[0m ' % (self.title))

        return result is not None

    def saveTmdbMovieResult(self, result):
        if hasattr(result, 'title'):
            self.title = result.title
        elif hasattr(result, 'original_title'):
            self.title = result.original_title
        # if hasattr(result, 'media_type'):
        #     self.ccfcat = transToCCFCat(result.media_type, self.ccfcat)
        self.tmdbid = result.id
        self.tmdbcat = 'movie'
        if hasattr(result, 'original_language'):
            if result.original_language == 'zh':
                self.original_language = 'cn'
            else:
                self.original_language = result.original_language
        if hasattr(result, 'popularity'):
            self.popularity = result.popularity
        if hasattr(result, 'poster_path'):
            self.poster_path = result.poster_path
        if hasattr(result, 'release_date'):
            self.year = self.getYear(result.release_date)
        elif hasattr(result, 'first_air_date'):
            self.year = self.getYear(result.first_air_date)
        else:
            self.year = 0
        if hasattr(result, 'genre_ids'):
            self.genre_ids = result.genre_ids
        
        print('Found [%d]: %s' % (self.tmdbid, self.title))
        return True

    def saveTmdbMultiResult(self, result):
        if hasattr(result, 'media_type'):
            self.imdbcat = result.media_type
            if result.media_type == 'tv':
                self.saveTmdbTVResultMatch(result)
            elif result.media_type == 'movie':
                self.saveTmdbMovieResult(result)
            else:
                print('Unknow media_type %s ' % result.media_type)
        return

    # def imdbMultiQuery(self, title, year=None):
    #     search = Search()
    #     return search.multi({"query": title, "year": year, "page": 1})

    # def sortByPopularity(resultList):
    #     newlist = sorted(resultList, key=lambda x: x.popularity, reverse=True)

    def getYear(self, datestr):
        intyear = 0
        m2 = re.search(
            r'\b((19\d{2}\b|20\d{2})(-19\d{2}|-20\d{2})?)',
            datestr,
            flags=re.A | re.I)
        if m2:
            yearstr = m2.group(2)
            intyear = int(yearstr)
        # m = re.match(r'^(\d+)\b', datestr)
        # if m:
        #     yearstr = m.group(0)
        #     intyear = int(yearstr)
        return intyear

    def findYearMatch(self, results, year, strict=True):
        for result in results:
            datestr = ''
            if hasattr(result, 'first_air_date'):
                datestr = result.first_air_date
            elif hasattr(result, 'release_date'):
                datestr = result.release_date

            resyear = self.getYear(datestr)
            if year == 0:
                return result

            if strict:
                if resyear == year:
                    return result
            else:
                if resyear in [year-3, year-2, year-1, year, year+1]:
                    self.year = resyear
                    return result
        return None

    def searchTMDb(self, title, cat=None, parseYearStr=None, cntitle=None):
        searchList = []
        if title == cntitle:
            cntitle = ''
        cuttitle = re.sub(r'\b(Extended|Anthology|Trilogy|Quadrilogy|Tetralogy|Collections?)\s*$', '', title, flags=re.I)
        cuttitle = re.sub(r'\b(Extended|HD|S\d+|V\d+|4K|CORRECTED)\s*$', '', cuttitle, flags=re.I)
        cuttitle = re.sub(r'(\d+部曲|全\d+集.*|原盘|系列|\s[^\s]*压制.*)\s*$', '', cuttitle, flags=re.I)
        cuttitle = re.sub(r'^\s*(剧集|BBC：?|TLOTR|Jade|Documentary|【[^】]*】)', '', cuttitle, flags=re.I)
        m1 = re.search(r'the movie\s*$', cuttitle, flags=re.A | re.I)
        if m1 and m1.span(0)[0] > 0:
            cuttitle = cuttitle[:m1.span(0)[0]].strip()
            cat = 'movie'

        m2 = re.search(
            r'\b((19\d{2}\b|20\d{2})(-19\d{2}|-20\d{2})?)\b(?!.*\b\d{4}\b.*)',
            cuttitle,
            flags=re.A | re.I)
        if m2 and m2.span(1)[0] > 0:
            cuttitle = cuttitle[:m2.span(1)[0]].strip()
            cuttitle2 = cuttitle[m2.span(1)[1]:].strip()

        intyear = self.getYear(parseYearStr)

        if self.ccfcatHard:
            if cat.lower() == 'tv':
                searchList = [('tv', cntitle), ('tv', cuttitle)]
            elif cat.lower() == 'movie':
                searchList = [('movie', cntitle), ('movie', cuttitle)]
        else:
            if self.season:
                searchList = [('tv', cntitle), ('tv', cuttitle), ('multi', cuttitle)]
            elif cat.lower() == 'tv':
                searchList = [('multi', cntitle), ('tv', cuttitle), ('multi', cuttitle)]
            elif cat.lower() == 'hdtv':
                searchList = [('multi', cntitle), ('multi', cuttitle)]
            elif cat.lower() == 'movie':
                searchList = [('movie', cntitle), ('movie', cuttitle), ('multi', cntitle), ('multi', cuttitle)]
            else:
                searchList = [('multi', cntitle), ('multi', cuttitle)]

        for s in searchList:
            if s[0] == 'tv' and s[1]:
                print('Search TV: ' + s[1])
                # tv = TV()
                # results = tv.search(s[1])
                search = Search()
                results = search.tv_shows({"query": s[1], "year": str(intyear), "page": 1})
                if len(results) > 0:
                    if intyear > 0 and self.season != 'S01':
                        intyear = 0
                    result = self.findYearMatch(results, intyear, strict=True)
                    if result:
                        self.saveTmdbTVResultMatch(result)
                        return self.tmdbid, self.title, self.year
                    else:
                        result = self.findYearMatch(results, intyear, strict=False)
                        if result:
                            self.saveTmdbTVResultMatch(result)
                            return self.tmdbid, self.title, self.year

            elif s[0] == 'movie' and s[1]:
                print('Search Movie:  %s (%d)' % (s[1], intyear))
                search = Search()
                if intyear == 0:
                    results = search.movies({"query": s[1], "page": 1})
                else:
                    results = search.movies({"query": s[1], "year": str(intyear), "page": 1})

                if len(results) > 0:
                    result = self.findYearMatch(results, intyear, strict=True)
                    if result:
                        self.saveTmdbMovieResult(result)
                        return self.tmdbid, self.title, self.year
                    else:
                        result = self.findYearMatch(results, intyear, strict=False)
                        if result:
                            self.saveTmdbMovieResult(result)
                            return self.tmdbid, self.title, self.year
                elif intyear > 0:
                    results = search.movies({"query": s[1], "page": 1})
                    if len(results) > 0:
                        result = self.findYearMatch(results, intyear, strict=False)
                        if result:
                            self.saveTmdbMovieResult(result)
                            return self.tmdbid, self.title, self.year
            elif s[0] == 'multi' and s[1]:
                print('Search Multi:  %s (%d)' % (s[1], intyear))
                search = Search()
                if intyear == 0:
                    results = search.multi({"query": s[1], "page": 1})
                else:
                    results = search.multi({"query": s[1], "year": str(intyear), "page": 1})

                if len(results) > 0:
                    result = self.findYearMatch(results, intyear, strict=True)
                    if result:
                        self.saveTmdbMultiResult(result)
                        return self.tmdbid, self.title, self.year
                    else:
                        result = self.findYearMatch(results, intyear, strict=False)
                        if result:
                            self.saveTmdbMultiResult(result)
                            return self.tmdbid, self.title, self.year
                elif intyear > 0:
                    results = search.multi({"query": s[1], "page": 1})
                    if len(results) > 0:
                        result = self.findYearMatch(results, intyear, strict=True)
                        if result:
                            self.saveTmdbMultiResult(result)
                            return self.tmdbid, self.title, self.year
                        else:
                            result = self.findYearMatch(results, intyear, strict=False)
                            if result:
                                self.saveTmdbMultiResult(result)
                                return self.tmdbid, self.title, self.year

        print('\033[31mTMDb Not found: [%s] [%s]\033[0m ' % (title, cntitle))
        return 0, title, intyear

