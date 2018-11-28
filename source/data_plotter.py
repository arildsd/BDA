import numpy as np
import matplotlib.pyplot as plt
import codecs

if __name__ == '__main__':
    input_file = codecs.open(r"../data/users_with_aggregated_features.tab", mode="r", encoding="utf-8")
    header = input_file.readline().replace("\r\n", "").split("\t")
    print(header)
    feature_matrix = []
    for line in input_file:
        l_a = line.split("\t")
        features = [l_a[0]]
        for i in range(1, len(l_a)):
            features.append(int(l_a[i]))
        feature_matrix.append(features)
    feature_dict = {}
    for i in range(1, len(header)):
        feature_list = [user_list[i] for user_list in feature_matrix]
        feature_dict[header[i]] = np.array(feature_list)
    # Histogram plots
    for f in header[1:]:
        features = feature_dict[f]
        ma = np.max(features)
        print("The max value for %s was %d" % (f, ma))
        mi = np.min(features)
        print("The min value for %s was %d" % (f, mi))
        plt.hist(features, bins=np.linspace(mi, ma, 10))
        plt.title(f)
        plt.show()
    # Box plots
    for f in header[1:]:
        features = feature_dict[f]
        ma = np.max(features)
        print("The max value for %s was %d" % (f, ma))
        mi = np.min(features)
        print("The min value for %s was %d" % (f, mi))
        plt.boxplot(features, showfliers=False)
        plt.title(f)
        plt.show()
    for f_1 in header[1:]:
        for f_2 in header[1:]:
            if f_1 == f_2: continue
            plt.scatter(feature_dict[f_1], feature_dict[f_2])
            plt.title("%s %s scatter" % (f_1, f_2))
            plt.xlabel(f_1)
            plt.ylabel(f_2)
            plt.show()


