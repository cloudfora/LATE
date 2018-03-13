import os
home = os.environ['HOME']

# MODE
# step1/rand_init for pre-training on ref (step1)
# step2/rand_init for one step training (late)
# step2/load_saved for transfer learning (translate)
mode = 'late'  # pre-training, translate, late
mse_mode = 'mse_omega'  # mse_omega, mse
data_transformation = 'log'  # as_is/log/rpm_log/exp_rpm_log (done on H)

if mode == 'pre-training':
    # Reference Pretraining
    stage = 'step1'
    run_flag = 'rand_init'
elif mode == 'translate':
    # Translate
    stage = 'step2'  # step1/step2 (not others)
    run_flag = 'load_saved'  # rand_init/load_saved
elif mode == 'late':
    # Late
    stage = 'step2'
    run_flag = 'rand_init'
else:
    raise Exception('mode err')

# HYPER PARAMETERS
L = 3  # only a reporter, changing it can't alter the model structure
l = L//2
n_hidden_1 = 200
# n_hidden_2 = 800  # update for different depth
# n_hidden_3 = 200
# n_hidden_4 = 100 # add more after changing model structure


# TRAINING PARAMETERS
pIn = 0.8
pHidden = 0.5
reg_coef = 0.0  # reg3=1e-2, can set to 0.0

if run_flag == 'rand_init':
    learning_rate = 3e-4  # step1: 3e-4 for 3-7L, 3e-5 for 9L
elif run_flag == 'load_saved':
    learning_rate = 3e-5  # step2: 3e-5 for 3-7L, 3e-6 for 9L
sd = 1e-3  # 3-7L:1e-3, 9L:1e-4, update for different depth
batch_size = 256
sample_size = int(9e4)  # todo: for test

max_training_epochs = int(1e3)
display_step = 50  # interval on learning curve
snapshot_step = int(5e2)  # interval of saving session, imputation

[a, b, c] = [0.7, 0.15, 0.15]  # splitting proportion: train/valid/test

patience = 5  # early stop patience epochs, just print warning, early stop not implemented yet


# BMB.MAGIC
# file1 = 'saver.hd5'
# file1 = '/Volumes/radio/audrey2/imputation/data/10x_human_pbmc_68k' \
#         '/filtering/10x_human_pbmc_68k.g949.hd5'
file1 = '/Volumes/radio/audrey2/imputation/data/10x_mouse_brain_1.3M' \
        '/1M_neurons_matrix_subsampled_20k_filtered.h5'
genome1 = 'mm10'  # only for 10x_genomics sparse matrix h5 data
name1 = 'test'
file1_orientation = 'gene_row'  # cell_row/gene_row

# For development usage #
seed_tf = 3
test_flag = 0  # [0, 1], in test mode only 10000 gene, 1000 cells tested
if test_flag == 1:
    max_training_epochs = 10 # 3L:100, 5L:1000, 7L:1000, 9L:3000
    display_step = 1  # interval on learning curve
    snapshot_step = 5  # interval of saving session, imputation
    m = 1000
    n = 300
    sample_size = int(240)  # todo: for test


# Gene list (data frame index)
# Gene list
pair_list = [
    # TEST
    [2, 3],

    # # PBMC G5561 Non-Linear
    # ['ENSG00000173372',
    # 'ENSG00000087086'],
]

gene_list = [x for pair in pair_list for x in pair]


# print parameters
print('\nfile1:', file1)
print('name1:', name1)
print('data_frame1_orientation:', file1_orientation)
print('\nfile2:', file1)
print('name2:', name1)
print('data_frame2_orientation:', file1_orientation)

print()

print('Parameters:')
print('mode:', mode)
print('mse_mode:', mse_mode)
print('data_transformation:', data_transformation)
print('stage:', stage)
print('init:', run_flag)
print('test_mode:', test_flag)
print('{}L'.format(L))
# print('{} Genes'.format(n))
for l_tmp in range(1, l+1):
  print("n_hidden{}: {}".format(l_tmp, eval('n_hidden_'+str(l_tmp))))

print('learning_rate:', learning_rate)
print('reg_coef:', reg_coef)
print('batch_size:', batch_size)
print('sample_zie: ', sample_size)
print('data split: [{}/{}/{}]'.format(a,b,c) )
print('pIn:', pIn)
print('pHidden:', pHidden)
print('max_training_epochs:', max_training_epochs)
print('display_step', display_step)
print('snapshot_step', snapshot_step)
print()

