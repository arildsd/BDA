import numpy as np
import matplotlib.pyplot as plt
import codecs
import sklearn.decomposition as sk_de
import sklearn.preprocessing as sk_pre

# Global constants
SAVE = True
FIGURE_FILE_PATH = "../data/figures/"
OUTPUT_TABLE_FILE_PATH = "../data/tables"

SHOW = False


def quartiles(array):
    array = np.array(array)
    sorted_array = np.sort(array.copy())
    lower_index = len(sorted_array)/4
    higher_index = 3 * len(sorted_array)/4
    lower_value = sorted_array[lower_index]
    higher_value = sorted_array[higher_index]
    return higher_value, lower_value


def split(feature_matrix, feature_index):
    ads = []
    non_ads = []
    for i in range(len(feature_matrix)):
        if feature_matrix[i][-1]:
            ads.append(feature_matrix[i][feature_index])
        else:
            non_ads.append(feature_matrix[i][feature_index])

    return ads, non_ads

def get_color_map(feature_matrix):
    c = []
    for user_list in feature_matrix:
        is_advertiser = user_list[-1]
        if is_advertiser:
            c.append("RED")
        else:
            c.append("BLUE")
    return c


if __name__ == '__main__':
    plt.close("all")
    input_file = codecs.open(r"../data/users_with_aggregated_features.tab", mode="r", encoding="utf-8")
    header = input_file.readline().replace("\r\n", "").replace("\n", "").split("\t")
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
        if SAVE: plt.savefig(FIGURE_FILE_PATH + "histograms/raw/" + f + "_histogram")
        if SHOW: plt.show()
        plt.clf()

    # Outlier removed histogram
    for f in header[1:]:
        features = feature_dict[f]
        h_v, l_v = quartiles(features)
        iqr = h_v - l_v
        max_limit = h_v + 3 * iqr
        plt.hist(np.clip(features, 0, max_limit))
        plt.title(f + " with overflow limit at %d" % max_limit)
        if SAVE: plt.savefig(FIGURE_FILE_PATH + "histograms/overflow/" + f + " with_overflow_limit_at_%d" % max_limit + "_histogram")
        if SHOW: plt.show()
        plt.clf()

    # Dual histograms
    for f in range(1, len(header)):
        features = [feature_matrix[i][f] for i in range(len(feature_matrix))]
        ads, non_ads = split(feature_matrix, f)
        h_v, l_v = quartiles(features)
        iqr = h_v - l_v
        max_limit = h_v + 3 * iqr
        ads = np.clip(ads, 0, max_limit)
        non_ads = np.clip(non_ads, 0, max_limit)
        print("Ads, non_ads: ", ads, non_ads)
        plt.hist([ads, non_ads])
        plt.title(header[f] + " dual, with overflow limit at %d" % max_limit)
        if SAVE: plt.savefig(FIGURE_FILE_PATH + "histograms/dual/" + header[f] + " with_overflow_limit_at_%d" % max_limit + "_histogram")
        if SHOW: plt.show()
        plt.clf()

    # Box plots
    for f in header[1:]:
        features = feature_dict[f]
        ma = np.max(features)
        print("The max value for %s was %d" % (f, ma))
        mi = np.min(features)
        print("The min value for %s was %d" % (f, mi))
        plt.boxplot(features, showfliers=False)
        plt.title(f)
        if SAVE: plt.savefig(FIGURE_FILE_PATH + "box_plots/single/" + f + "_box_plot")
        if SHOW: plt.show()
        plt.clf()

    # Multiple box plots
    for f in range(1, len(header)-1):
        ads, non_ads = split(feature_matrix, f)
        plt.boxplot([ads, non_ads], showfliers=False)
        plt.title(header[f])
        plt.xticks([1, 2], ['ads', 'non_ads'])
        if SAVE: plt.savefig(FIGURE_FILE_PATH + "box_plots/dual/" + header[f] + "_box_plot")
        if SHOW: plt.show()
        plt.clf()

    # PCA using scikit
    np_matrix = np.array(feature_matrix)
    np_matrix = np_matrix[:,1:-1]
    np_matrix = sk_pre.scale(np_matrix)

    pca = sk_de.PCA(n_components=2)
    pca_matrix = pca.fit_transform(np_matrix)
    pc_1 = pca.components_[0]
    pc_2 = pca.components_[1]
    if SAVE:
        pca_table_file = open(OUTPUT_TABLE_FILE_PATH + "/pca.csv", "w")
        header_string = ";".join([""] + header[1:-1])
        pca_strings = [";".join(["pc_1"] + [str(e) for e in pc_1]), ";".join(["pc_2"] + [str(e) for e in pc_2])]
        result_string = "\n".join([header_string] + pca_strings)
        pca_table_file.write(result_string)
        pca_table_file.close()

    x = pca_matrix[:, 0]
    y = pca_matrix[:, 1]
    plt.scatter(x, y, c=get_color_map(feature_matrix), s=1)
    plt.title("PCA plot")
    if SAVE: plt.savefig(FIGURE_FILE_PATH + "scatter/PCA/2D_pca")
    if SHOW or True: plt.show()
    plt.clf()

    # Scatter plots for all combinations of features
    for f_1 in header[1:]:
        for f_2 in header[1:]:
            if f_1 == f_2: continue
            plt.scatter(feature_dict[f_1], feature_dict[f_2])
            plt.title("%s %s scatter" % (f_1, f_2))
            plt.xlabel(f_1)
            plt.ylabel(f_2)
            if SAVE: plt.savefig(FIGURE_FILE_PATH + "scatter/raw/" + f_1 + "_" + f_2 + "_scatter")
            if SHOW: plt.show()
            plt.clf()

    # Scatter plots for all combinations of features using log scale
    for f_1 in header[1:]:
        for f_2 in header[1:]:
            if f_1 == f_2: continue
            plt.scatter(np.log(feature_dict[f_1]), np.log(feature_dict[f_2]))
            plt.title("%s %s scatter with log scales" % (f_1, f_2))
            plt.xlabel("Log of " + f_1)
            plt.ylabel("Log of " + f_2)
            if SAVE: plt.savefig(FIGURE_FILE_PATH + "scatter/log/" + f_1 + "_" + f_2 + "_scatter_with_log")
            if SHOW: plt.show()
            plt.clf()

    # Plot with classes marked
    for f_1 in range(1, len(header)-1):
        for f_2 in range(1, len(header)-1):
            if f_1 == f_2: continue
            x = [feature_matrix[i][f_1] for i in range(len(feature_matrix))]
            y = [feature_matrix[i][f_2] for i in range(len(feature_matrix))]
            c = get_color_map(feature_matrix)
            plt.scatter(x, y, c=c)
            plt.title("%s %s scatter" % (header[f_1], header[f_2]))
            plt.xlabel(header[f_1])
            plt.ylabel(header[f_2])
            if SAVE: plt.savefig(FIGURE_FILE_PATH + "scatter/classified/" + header[f_1] + "_" + header[f_2] + "_scatter")
            if SHOW: plt.show()
            plt.clf()


