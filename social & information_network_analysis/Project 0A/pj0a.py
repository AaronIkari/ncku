import csv
import operator

''' global variable '''
TOP_K = 20
ATTR = ['gp', 'pts', 'reb', 'asts', 'stl', 'blk', 'turnover', 'fga', 'fgm', 'fta', 'ftm', 'eff_season_i']


''' read data from .csv file '''
def read():

    # open nba_data.csv file
    with open('nba_data.csv', 'r') as csvfile:
        # delimiter ','
        rows = csv.reader(csvfile, delimiter=',')
        # jump header(e.g., first line)
        next(rows)
        # strip white space in each cell
        rows = [ [x.strip() for x in row] for row in rows ]

    return rows

''' write Top-K to .txt file '''
def write(sort_eff_career, id_name_dict):

    with open('result.txt', 'w') as file:
        for idx in range(0, TOP_K):
            # write
            file.write('RANK %d\t%s\t%.2f\n' % (idx+1, id_name_dict[sort_eff_career[idx][0]], sort_eff_career[idx][1]))
            # print to stdout
            print 'RANK %d\t%s\t%.2f' % (idx+1, id_name_dict[sort_eff_career[idx][0]], sort_eff_career[idx][1])

'''main function'''
def main():

    # read data from .csv file
    rows = read() 
    
    # id-name dict (total: 4173)
    id_name_dict = dict()
    for row in rows:
        if row[0].upper() not in id_name_dict:
            id_name_dict[ row[0].upper() ] = row[2] + ' ' + row[3]


    nba_ids = dict()
    for row in rows:

        # if id not exist
        if row[0].upper() not in nba_ids:
            nba_ids[ row[0].upper() ] = dict()

        # if year not exist
        if row[1] not in nba_ids[ row[0].upper() ]:
            nba_ids[ row[0].upper() ][ row[1] ] = dict.fromkeys(ATTR, 0.0)

        # accumulate var if in same season
        nba_ids[ row[0].upper() ][ row[1] ]['gp'] += float(row[5])
        nba_ids[ row[0].upper() ][ row[1] ]['pts'] += float(row[7])
        nba_ids[ row[0].upper() ][ row[1] ]['reb'] += float(row[8])
        nba_ids[ row[0].upper() ][ row[1] ]['asts'] += float(row[9])

        # deal with 'stl' field missing value(e.g., NULL)
        if row[10] == 'NULL':
            nba_ids[ row[0].upper() ][ row[1] ]['stl'] += 0
        else: 
            nba_ids[ row[0].upper() ][ row[1] ]['stl'] += float(row[10])

        # deal with 'blk' field missing value(e.g., NULL)
        if row[11] == 'NULL':
            nba_ids[ row[0].upper() ][ row[1] ]['blk'] += 0
        else: 
            nba_ids[ row[0].upper() ][ row[1] ]['blk'] += float(row[11])

        # deal with 'turnover' field missing value(e.g., NULL)
        if row[12] == 'NULL':
            nba_ids[ row[0].upper() ][ row[1] ]['turnover'] += 0
        else:
            nba_ids[ row[0].upper() ][ row[1] ]['turnover'] += float(row[12])

        nba_ids[ row[0].upper() ][ row[1] ]['fga'] += float(row[13])
        nba_ids[ row[0].upper() ][ row[1] ]['fgm'] += float(row[14])
        nba_ids[ row[0].upper() ][ row[1] ]['fta'] += float(row[15])
        nba_ids[ row[0].upper() ][ row[1] ]['ftm'] += float(row[16])

    # calculate eff_season_i value for each player at each season
    for nba_id in nba_ids:
        for season in nba_ids[nba_id]:
            nba_ids[nba_id][season]['eff_season_i'] = (nba_ids[nba_id][season]['pts'] +
                                                       nba_ids[nba_id][season]['reb'] +
                                                       nba_ids[nba_id][season]['asts'] + 
                                                       nba_ids[nba_id][season]['stl'] + 
                                                       nba_ids[nba_id][season]['blk'] - 
                                                       nba_ids[nba_id][season]['fga'] + 
                                                       nba_ids[nba_id][season]['fgm'] - 
                                                       nba_ids[nba_id][season]['fta'] + 
                                                       nba_ids[nba_id][season]['ftm'] - 
                                                       nba_ids[nba_id][season]['turnover']) / nba_ids[nba_id][season]['gp']

    eff_career = dict()
    for nba_id in nba_ids:

        # if id not in eff_career
        if nba_id not in eff_career:
            eff_career[nba_id] = 0.0

        # number of season
        counter = 0
        # tmp value sum up eff_season_i value
        total = 0
        for season in nba_ids[nba_id]:
            # sum up eff_season_i value at each season for this player
            total += nba_ids[nba_id][season]['eff_season_i']
            counter += 1

        # calculate eff_career value for each player
        eff_career[nba_id] = total / counter


    # sort eff_career in decreasing order
    sort_eff_career = sorted(eff_career.items(), key=operator.itemgetter(1), reverse=True)
    
    # write Top-K to .txt file
    write(sort_eff_career, id_name_dict)

''' main function '''
if __name__ == "__main__":
    main()
