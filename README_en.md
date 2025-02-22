# torcp
A script to organize media files in Emby-happy way, create hardlink in a seperate dir:
1. Category TV/Movie.
2. Parse movie name, year, season from filename/dirname.
3. Rename and organize your media files  in [Emby-happy](https://support.emby.media/support/solutions/articles/44001159102-movie-naming) ways:
4. create `Hard Link` ( ln ) to a seperate dir
 

##  Usage:
```sh 
python3 torcp.py -h
```

```
usage: torcp.py [-h] [-d HD_PATH] [--tv] [--movie] [--dryrun] [--single] [--extract-bdmv] [--full-bdmv]
                [--origin-name]
                MEDIA_DIR

torcp: a script hardlink media files and directories in Emby-happy naming and structs.

positional arguments:
  MEDIA_DIR             The directory contains TVs and Movies to be copied.

optional arguments:
  -h, --help            show this help message and exit
  -d HD_PATH, --hd_path HD_PATH
                        the dest path to create Hard Link.
  --tv                  specify the src directory is TV.
  --movie               specify the src directory is Movie.
  --dryrun              print message instead of real copy.
  --single, -s          parse and copy one single folder.
  --extract-bdmv        extract largest file in BDMV dir.
  --full-bdmv           copy full BDMV dir and iso files.
  --origin-name         keep origin file name.
```
##  Examples:

* hardlink whole dir to a seperate dir, with guessed category:
```sh 
python3 torcp.py /home/ccf2012/Downloads/  -d /home/ccf2012/emby/ 
```

* hardlink, specify ALL subdirs are Movie:
```sh
python3 torcp.py /home/ccf2012/Downloads/RSSMovie/ -d /home/ccf2012/emby/ --movie
```

* hardlink, specify one SINGLE dir is TV:
```sh
python3 torcp.py /home/ccf2012/Downloads/权力的游戏.第1-8季.Game.Of.Thrones.S01-S08.1080p.Blu-Ray.AC3.x265.10bit-Yumi -d /home/ccf2012/emby/ -s --tv
```


### BDMV option:
1. default, skip all dir with `BDMV` inside and `.iso` file
```sh
python3 torcp.py /volume1/video/emby/test -d /volume1/video/emby/testdir
```
2. `--extract-bdmv` option, extract largest file(s) from BDMV dir, of movie/tv
> with `iso` files copy to sepereate dir
```sh
python3 torcp.py /volume1/video/emby/test -d /volume1/video/emby/testdir --extract-bdmv
```
3. `--full-bdmv` option, copy the full BDMV dir and `.iso` file 
```sh
python3 torcp.py /volume1/video/emby/test -d /volume1/video/emby/testdir --full-bdmv
```



## Acknowledgement 
Special thank to Aruba@hutongyouwu & @ozz
@NishinoKana @Esc @Hangsijing 


## Update 2022.2.5 @dev 

* 减了rclone copy功能，只作硬链。需要rclone copy就硬链出来另外命令拷
* 还有quickskip, no_nfo等功能也都减了
* MovieEncode只收mkv, mp4, 其它jpg,nfo等小文件都不链了

* 主要变化是各目录进去看里面文件进行识别。
    里面有BDMV目录或iso都移到MovieBDMV目录
    外面目录识别不出tv，到里面可能识别出，movie tv识别有概率更稳了
    还有目录中有多文件的，比如smurf 1-3 这样的目录会进去挨个识别分别开出3个目录
    还有是带collections pack这样的目录会进去分别识别

## Update 2022.2.9 @dev
* Rename TV episode name with `S01E01` and `-EncodeGroup`, like this:
```
[/share/CACHEDEV1_DATA/Video/emby/TV/Loki (2021)] # tree . -A
.
└── S01
    ├── Loki\ S01E01\ -\ AJ.mkv
    ├── Loki\ S01E01\ -\ CHDBits.mkv
    ├── Loki\ S01E02\ -\ AJ.mkv
    ├── Loki\ S01E02\ -\ CHDBits.mkv
    ├── Loki\ S01E03\ -\ AJ.mkv
    ├── Loki\ S01E03\ -\ CHDBits.mkv
    ├── Loki\ S01E04\ -\ AJ.mkv
    ├── Loki\ S01E04\ -\ CHDBits.mkv
    ├── Loki\ S01E05\ -\ AJ.mkv
    ├── Loki\ S01E05\ -\ CHDBits.mkv
    ├── Loki\ S01E06\ -\ AJ.mkv
    └── Loki\ S01E06\ -\ CHDBits.mkv
```

* New `--extract-bdmv` param, Extract Largest file(s) from BDMV dir, of movie/tv
  
### Sample
* Command:
```sh
python torcp.py  /share/CACHEDEV1_DATA/Video/QB/TV  -d /share/CACHEDEV1_DATA/Video/emby/  --extract-bdmv 
```
* Before:
```
[/share/CACHEDEV1_DATA/Video/QB/TV/Civilisations.S01.COMPLETE.BLURAY-VEXHD] # tree . -h -A -P *.m2ts
.
├── [4.0K]  CIVILISATIONS_D1
│   └── [4.0K]  BDMV
│       ├── [4.0K]  BACKUP
│       │   ├── [4.0K]  CLIPINF
│       │   └── [4.0K]  PLAYLIST
│       ├── [4.0K]  CLIPINF
│       ├── [4.0K]  META
│       │   └── [4.0K]  DL
│       ├── [4.0K]  PLAYLIST
│       └── [4.0K]  STREAM
│           ├── [ 14G]  00002.m2ts
│           ├── [ 14G]  00003.m2ts
│           ├── [ 14G]  00004.m2ts
│           ├── [1.1M]  00005.m2ts
│           ├── [ 12M]  00006.m2ts
│           ├── [ 94M]  00007.m2ts
│           ├── [ 94M]  00008.m2ts
│           ├── [1.9M]  00009.m2ts
│           ├── [1.5M]  00010.m2ts
│           └── [126K]  00011.m2ts
├── [4.0K]  CIVILISATIONS_D2
│   └── [4.0K]  BDMV
│       ├── [4.0K]  BACKUP
│       │   ├── [4.0K]  CLIPINF
│       │   └── [4.0K]  PLAYLIST
│       ├── [4.0K]  CLIPINF
│       ├── [4.0K]  META
│       │   └── [4.0K]  DL
│       ├── [4.0K]  PLAYLIST
│       └── [4.0K]  STREAM
│           ├── [ 14G]  00002.m2ts
│           ├── [ 14G]  00003.m2ts
│           ├── [ 14G]  00004.m2ts
│           ├── [1.1M]  00005.m2ts
│           ├── [ 12M]  00006.m2ts
│           ├── [ 94M]  00007.m2ts
│           ├── [ 94M]  00008.m2ts
│           ├── [1.9M]  00009.m2ts
│           ├── [1.5M]  00010.m2ts
│           └── [126K]  00011.m2ts
└── [4.0K]  CIVILISATIONS_D3
    └── [4.0K]  BDMV
        ├── [4.0K]  BACKUP
        │   ├── [4.0K]  CLIPINF
        │   └── [4.0K]  PLAYLIST
        ├── [4.0K]  CLIPINF
        ├── [4.0K]  META
        │   └── [4.0K]  DL
        ├── [4.0K]  PLAYLIST
        └── [4.0K]  STREAM
            ├── [ 14G]  00002.m2ts
            ├── [ 14G]  00003.m2ts
            ├── [ 14G]  00004.m2ts
            ├── [1.1M]  00005.m2ts
            ├── [ 12M]  00006.m2ts
            ├── [ 94M]  00007.m2ts
            ├── [ 94M]  00008.m2ts
            ├── [1.9M]  00009.m2ts
            ├── [1.5M]  00010.m2ts
            └── [126K]  00011.m2ts

```
* After:
```
[/share/CACHEDEV1_DATA/Video/emby/BDMV_TV/Civilisations] # tree . -h -A
.
├── [4.0K]  CIVILISATIONS_D1
│   ├── [ 14G]  CIVILISATIONS_D1\ -\ 00002.m2ts
│   ├── [ 14G]  CIVILISATIONS_D1\ -\ 00003.m2ts
│   └── [ 14G]  CIVILISATIONS_D1\ -\ 00004.m2ts
├── [4.0K]  CIVILISATIONS_D2
│   ├── [ 14G]  CIVILISATIONS_D2\ -\ 00002.m2ts
│   ├── [ 14G]  CIVILISATIONS_D2\ -\ 00003.m2ts
│   └── [ 14G]  CIVILISATIONS_D2\ -\ 00004.m2ts
└── [4.0K]  CIVILISATIONS_D3
    ├── [ 14G]  CIVILISATIONS_D3\ -\ 00002.m2ts
    ├── [ 14G]  CIVILISATIONS_D3\ -\ 00003.m2ts
    └── [ 14G]  CIVILISATIONS_D3\ -\ 00004.m2ts

```

## Update 2022.2.10 @dev
* add `--full-bdmv` option: copy the full BDMV dir and `.iso` file 
* add `--origin-name` option: keep the origin filename of `.mkv` and `.mp4`, both for movie and tv
