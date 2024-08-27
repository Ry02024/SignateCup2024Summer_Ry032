# src/evaluate_model.py の冒頭に追加

import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

def focal_loss(y_true, y_pred, alpha=0.25, gamma=2.0):
    pt = np.where(y_true == 1, y_pred, 1 - y_pred)
    loss = -alpha * (1 - pt) ** gamma * np.log(pt)
    return loss

def focal_loss_lgb(y_pred, dtrain, alpha=0.25, gamma=2.0):
    y_true = dtrain.get_label()
    y_pred = 1.0 / (1.0 + np.exp(-y_pred))
    pt = np.where(y_true == 1, y_pred, 1 - y_pred)
    fl = focal_loss(y_true, y_pred, alpha, gamma)
    grad = alpha * y_pred * (1 - y_pred) * (gamma * (1 - pt) ** (gamma - 1) * np.log(pt) + (1 - pt) ** gamma / pt) * (2 * y_true - 1)
    hess = alpha * (1 - y_pred) * y_pred * (
        (1 - pt) ** (gamma - 2) * (
            (2 * gamma * (1 - pt) + gamma * (gamma - 1) * (1 - pt) + 1) * np.log(pt)
            + 2 * (1 - pt)
        ) - (1 - pt) ** gamma / pt ** 2
    ) * (2 * y_true - 1) ** 2
    return grad, hess

def weighted_cross_entropy(weight_positive=2.0):
    def weighted_cross_entropy_obj(y_pred, dtrain):
        y_true = dtrain.get_label()
        y_pred = 1.0 / (1.0 + np.exp(-y_pred))
        grad = (y_pred - y_true) * (weight_positive * y_true + (1 - y_true))
        hess = y_pred * (1.0 - y_pred) * (weight_positive * y_true + (1 - y_true))
        return grad, hess
    return weighted_cross_entropy_obj

def dice_loss(smooth=1e-6):
    def dice_loss_obj(y_pred, dtrain):
        y_true = dtrain.get_label()
        y_pred = 1.0 / (1.0 + np.exp(-y_pred))
        intersection = np.sum(y_true * y_pred)
        union = np.sum(y_true) + np.sum(y_pred)
        dice = (2.0 * intersection + smooth) / (union + smooth)
        grad = -2 * (y_true * (union - y_pred) - y_pred * (intersection + smooth)) / (union + smooth)**2
        hess = 2 * ((union - y_pred)**2 + y_pred * (intersection + smooth)) / (union + smooth)**3
        return grad, hess
    return dice_loss_obj

def balanced_cross_entropy():
    def balanced_cross_entropy_obj(y_pred, dtrain):
        y_true = dtrain.get_label()
        y_pred = 1.0 / (1.0 + np.exp(-y_pred))
        pos_weight = np.sum(1 - y_true) / np.sum(y_true)
        grad = y_pred - y_true
        hess = y_pred * (1.0 - y_pred)
        grad *= np.where(y_true == 1, pos_weight, 1.0)
        hess *= np.where(y_true == 1, pos_weight, 1.0)
        return grad, hess
    return balanced_cross_entropy_obj

def asymmetric_loss(gamma_neg=4, gamma_pos=1):
    def asymmetric_loss_obj(y_pred, dtrain):
        y_true = dtrain.get_label()
        y_pred = 1.0 / (1.0 + np.exp(-y_pred))
        pt = np.where(y_true == 1, y_pred, 1 - y_pred)
        grad = y_pred - y_true
        hess = y_pred * (1.0 - y_pred)
        grad *= np.where(y_true == 1, gamma_pos * (1 - pt)**(gamma_pos - 1), gamma_neg * pt**(gamma_neg - 1))
        hess *= np.where(y_true == 1, gamma_pos * (1 - pt)**(gamma_pos - 1), gamma_neg * pt**(gamma_neg - 1))
        return grad, hess
    return asymmetric_loss_obj

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

from sklearn.metrics import roc_auc_score, average_precision_score

def auc_eval(y_pred, dtrain):
    y_true = dtrain.get_label()
    return 'auc', roc_auc_score(y_true, y_pred), True

def pr_auc_eval(y_pred, dtrain):
    y_true = dtrain.get_label()
    return 'pr_auc', average_precision_score(y_true, y_pred), True
