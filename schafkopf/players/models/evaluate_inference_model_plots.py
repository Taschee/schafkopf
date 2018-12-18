import matplotlib.pyplot as plt
from schafkopf.players.data.load_data import num_games_in_file


thresholds = [0.001, 0.005, 0.01, 0.015, 0.02, 0.03, 0.05, 0.1, 0.15000000000000002, 0.2, 0.25, 0.30000000000000004, 0.35000000000000003, 0.4, 0.45, 0.5, 0.55, 0.6000000000000001, 0.65, 0.7000000000000001, 0.75, 0.8, 0.8500000000000001, 0.9, 0.9500000000000001, 0.99]


num_games_solo = num_games_in_file('../data/test_data_solo.p')
num_games_wenz = num_games_in_file('../data/test_data_wenz.p')
num_games_partner = num_games_in_file('../data/test_data_partner.p')


accuracies_solo = [0.18656352516150465, 0.25040410362252025, 0.2952363783856866, 0.3143047401174231, 0.3244600869148532,
                   0.3359061365963591, 0.3504456352045063, 0.375468472858878, 0.39238518241046705, 0.4063424391525894,
                   0.42030425231959606, 0.4363004822990868, 0.4558156091483492, 0.47930930568948893, 0.5070730125368429,
                   0.5417167220220008, 0.5866302864938608, 0.6415736420119106, 0.7004273819173237, 0.7555690256099409,
                   0.8052702702702703, 0.8479860217031451, 0.8885108610311436, 0.9334669338677355, 0.9767972613160898,
                   0.9912854030501089]
accuracies_wenz = [0.16940401467243643, 0.207739178145485, 0.24553515034192674, 0.2694933363324523, 0.28522364058684563,
                   0.3043627750611247, 0.3236259769039694, 0.3460311710787125, 0.36146232493233627, 0.3755506536687604,
                   0.38847746090156393, 0.4014680704144083, 0.414751717657396, 0.43055170953397076, 0.4526612539467749,
                   0.480916274754455, 0.516091741422362, 0.558817615121657, 0.6099387338325392, 0.6611188811188812,
                   0.7297242083758938, 0.7859462651313847, 0.8403470715835141, 0.9000684462696783, 0.9368556701030928,
                   0.9929577464788732]
accuracies_partner = [0.23075312909419135, 0.3208712139203886, 0.33223830569140617, 0.3356925860699358,
                      0.3377281598216617, 0.34054074826180786, 0.34466917116694057, 0.35394023859309653,
                      0.3647043769973656, 0.37847533936115074, 0.3948749422599224, 0.4148928856200654,
                      0.44062376657746344, 0.47494868126399603, 0.5174121932266268, 0.5655079030091944,
                      0.6138481588317729, 0.661810043975649, 0.7089967537486473, 0.757091379469648,
                      0.8033961376419513, 0.8474087721383573, 0.8903728670739415, 0.9322002007024586,
                      0.9696173254835997, 0.9892715979672502]

prediction_numbers_solo = [842855, 627933, 532536, 500072, 484152, 466806, 444534, 404239, 373745, 342455, 305010,
                           260834, 213503, 165920, 121801, 84906, 57174, 38789, 27142, 19797, 14800, 10874, 7642,
                           4990, 2629, 459]
prediction_numbers_solo = [num / (num_games_solo * 26) for num in prediction_numbers_solo]
prediction_numbers_wenz = [424742, 346290, 292899, 266745, 251855, 235584, 220211, 198774, 177717, 154589, 130440,
                           105717, 81943, 61391, 44340, 31257, 21626, 14919, 10283, 7150, 4895, 3387, 2305,
                           1461, 776, 142]
prediction_numbers_wenz = [num / (num_games_wenz * 26) for num in prediction_numbers_wenz]
prediction_numbers_partner = [3191259, 2294821, 2216078, 2192926, 2179229, 2159859, 2129500, 2050688, 1938178,
                              1771122, 1547885, 1265423, 945033, 643040, 415657, 271036, 183389, 127798, 90566,
                              64938, 46759, 33652, 23735, 15944, 9512, 3542]
prediction_numbers_partner = [num / (num_games_partner * 26) for num in prediction_numbers_partner]

print([(thresh, num) for thresh, num in zip(thresholds, prediction_numbers_solo)])
print([(thresh, num) for thresh, num in zip(thresholds, prediction_numbers_wenz)])
print([(thresh, num) for thresh, num in zip(thresholds, prediction_numbers_partner)])

print([(thresh, acc * num - (1 - acc) * num) for thresh, acc, num in zip(thresholds, accuracies_solo, prediction_numbers_solo)])
print([(thresh, acc * num - (1 - acc) * num) for thresh, acc, num in zip(thresholds, accuracies_wenz, prediction_numbers_wenz)])
print([(thresh, acc * num - (1 - acc) * num) for thresh, acc, num in zip(thresholds, accuracies_partner, prediction_numbers_partner)])


fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_ylabel('Accuracy')
ax1.plot(thresholds, accuracies_solo, c='blue', label='Solo')
ax1.plot(thresholds, accuracies_wenz, c='red', label='Wenz')
ax1.plot(thresholds, accuracies_partner, c='green', label='Partner Mode')
ax2.set_ylabel('Predictions per game')
ax2.set_xlabel('Thresholds')
ax2.plot(thresholds, prediction_numbers_solo, c='blue', label='Solo')
ax2.plot(thresholds, prediction_numbers_wenz, c='red', label='Wenz')
ax2.plot(thresholds, prediction_numbers_partner, c='green', label='Partner Mode')
ax1.legend()
plt.show()
