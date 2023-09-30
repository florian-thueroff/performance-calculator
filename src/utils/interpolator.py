def build_param_model(config):

    # fit models
    fit_right_upper = FirstOrderRational(*config["FIT_UPPER_RIGHT"])
    pu_right = fit_right_upper.parameters()
    fit_right_mid = FirstOrderRational(*config["FIT_MID_RIGHT"])
    pm_right = fit_right_mid.parameters()
    fit_right_lower = FirstOrderRational(*config["FIT_LOWER_RIGHT"])
    pl_right = fit_right_lower.parameters()

    fit_left_upper = FirstOrderPolynomial(*config["FIT_UPPER_LEFT"])
    pu_left = fit_left_upper.parameters()
    fit_left_mid = FirstOrderPolynomial(*config["FIT_MID_LEFT"])
    pm_left = fit_left_mid.parameters()
    fit_left_lower = FirstOrderPolynomial(*config["FIT_LOWER_LEFT"])
    pl_left = fit_left_lower.parameters()

    # fit model for parameters
    pfit = {}
    for k, _ in pu_right.items():
        pfit[k] = [
            [fit_right_lower.model()(600), pl_right[k]],
            [fit_right_mid.model()(600), pm_right[k]],
            [fit_right_upper.model()(600), pu_right[k]],
        ]
    for k, _ in pu_left.items():
        pfit[k] = [
            [config["PH_LOWER"], pl_left[k]],
            [config["PH_MID"], pm_left[k]],
            [config["PH_UPPER"], pu_left[k]],
        ]
    
    # get models for parameters
    param_model = {}
    for k, pts in pfit.items():
        if k in ('b', 'c'):
            param_model[k] = SecondOrderRational(*pts)
        else:
            param_model[k] = SecondOrderPolynomial(*pts)
    
    return param_model