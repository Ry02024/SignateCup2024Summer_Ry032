import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

def max_score(preds, dif, test_y, over_value_sum=[0.0], depth=[0], max=[0.0], ensemble_pred=None, max_ratio=[0.0], now_ratio=[0.0]):
    """
    モデルの重みを最適化し、最大のAUCスコアを見つける関数。
    """
    if ensemble_pred is None:
        ensemble_pred = np.zeros(len(preds[0]))

    if len(preds) == depth[0] + 1:
        temp_ensemble_pred = np.copy(ensemble_pred)
        value = 1.0 - over_value_sum[0]
        now_ratio[depth[0]] = value
        ensemble_pred += preds[depth[0]] * value
        ensemble_auc = roc_auc_score(test_y, ensemble_pred)
        ensemble_pred = np.copy(temp_ensemble_pred)

        if ensemble_auc > max[0]:
            max[0] = ensemble_auc
            max_ratio[:] = now_ratio[:]
    elif depth[0] == 0:
        while over_value_sum[0] <= 1.0 + dif:
            max_score(preds, dif, test_y, over_value_sum, depth=[1], max=max, ensemble_pred=np.zeros(len(preds[0])), max_ratio=max_ratio, now_ratio=np.zeros(len(preds)))
            over_value_sum[0] += dif
        return [max[0], max_ratio]
    else:
        temp_ensemble_pred = np.copy(ensemble_pred)
        temp_over_value_sum = over_value_sum[0]
        while over_value_sum[0] <= 1.0:
            max_score(preds, dif, test_y, over_value_sum, depth=[depth[0] + 1], max=max, ensemble_pred=ensemble_pred, max_ratio=max_ratio, now_ratio=now_ratio)
            ensemble_pred += preds[depth[0]] * dif
            now_ratio[depth[0]] += dif
            over_value_sum[0] += dif
        ensemble_pred = np.copy(temp_ensemble_pred)
        over_value_sum[0] = temp_over_value_sum
        now_ratio[depth[0]] = 0.0

def max_score_2eval(preds, dif, test_y, over_value_sum=[0.0], depth=[0], best_score=[0.0], ensemble_pred=None, max_ratio=[0.0], now_ratio=[0.0]):
    """
    モデルの重みを最適化し、AUCとPRAUCの調和平均を最大化する関数。
    """
    if ensemble_pred is None:
        ensemble_pred = np.zeros(len(preds[0]))

    if len(preds) == depth[0] + 1:
        temp_ensemble_pred = np.copy(ensemble_pred)
        value = 1.0 - over_value_sum[0]
        now_ratio[depth[0]] = value
        ensemble_pred += preds[depth[0]] * value
        ensemble_auc = roc_auc_score(test_y, ensemble_pred)
        ensemble_prauc = average_precision_score(test_y, ensemble_pred)

        combined_score = 2 * (ensemble_auc * ensemble_prauc) / (ensemble_auc + ensemble_prauc) if ensemble_auc + ensemble_prauc > 0 else 0

        ensemble_pred = np.copy(temp_ensemble_pred)

        if combined_score > best_score[0]:
            best_score[0] = combined_score
            max_ratio[:] = now_ratio[:]
    elif depth[0] == 0:
        while over_value_sum[0] <= 1.0 + dif:
            max_score_2eval(preds, dif, test_y, over_value_sum, depth=[1], best_score=best_score, ensemble_pred=np.zeros(len(preds[0])), max_ratio=max_ratio, now_ratio=np.zeros(len(preds)))
            over_value_sum[0] += dif
        return [best_score[0], max_ratio]
    else:
        temp_ensemble_pred = np.copy(ensemble_pred)
        temp_over_value_sum = over_value_sum[0]
        while over_value_sum[0] <= 1.0:
            max_score_2eval(preds, dif, test_y, over_value_sum, depth=[depth[0] + 1], best_score=best_score, ensemble_pred=ensemble_pred, max_ratio=max_ratio, now_ratio=now_ratio)
            ensemble_pred += preds[depth[0]] * dif
            now_ratio[depth[0]] += dif
            over_value_sum[0] += dif
        ensemble_pred = np.copy(temp_ensemble_pred)
        over_value_sum[0] = temp_over_value_sum
        now_ratio[depth[0]] = 0.0
