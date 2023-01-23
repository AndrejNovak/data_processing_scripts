from DPE_functions import *
import os
import fnmatch

names = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
 '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']

subfolders = [ f.name for f in os.scandir('Q:/DPE_carlos_data_output/2022_12_VdG/2022_12_VdG_D05/') if f.is_dir() ]
print(subfolders[12:])

for idx2, var2 in enumerate(subfolders[12:]):
    directory = var2
    dir_path = 'Q:/DPE_carlos_data_output/2022_12_VdG/2022_12_VdG_D05/'+var2+'/Files/'
    count = len(fnmatch.filter(os.listdir(dir_path), '*.clog'))
    print('File Count:', count)

    for idx, var in enumerate(names[:count]):
        clog_poradie = var
        path = 'Q:/DPE_carlos_data_output/2022_12_VdG/2022_12_VdG_D05/' + directory + '/Files/ClusterLog_clog_r00000000' + clog_poradie + '.clog'
        clog = read_clog(path)[2]

        #print(len(read_clog(path)[3]), np.shape(read_clog(path)[3]), read_clog(path)[3][0:8])

        print(f'The number of frames in clog is {len(read_clog(path)[0])} with specific values {read_clog(path)[0]}')
        matrix = np.zeros([256,256])

        num_of_particles = np.array([len(clog[:]), 100])         #len(clog[:])

        print(clog_poradie)
        print(len(clog[:]))
        print(num_of_particles)

        for k in range(len(num_of_particles)):
            number = num_of_particles[k]

            for l in range(number):   #range(len(clog[:]))
                x = []
                y = []
                for m in range(len(clog[l][:])):
                    if len(clog[l][:]) > 0 and len(clog[l][:]) < 3000:
                        x.append(clog[l][m][0])
                        y.append(clog[l][m][1])
                        matrix[int(x[m]), int(y[m])] = matrix[int(x[m]), int(y[m])] + clog[l][m][2]
                    else:
                        pass

            clog_title = 'D05 Si 500um '+ directory + ' ' + str(num_of_particles[k]) + ' particles'
            OutputPath = './'
            OutputName = 'Si_500um_D05_' + directory + '_' + str(num_of_particles[k]) + '_particles_' + clog_poradie
            print_fig_E(matrix, 1E4, clog_title, OutputPath, OutputName)
