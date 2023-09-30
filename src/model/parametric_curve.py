from typing import Dict, List, Optional, Tuple, Type, Union
from model import Model
import matplotlib.pyplot as plt


class ParametricCurve:

    def __init__(
            self, 
            model: Type[Model], 
            param_model_dict: Dict[str, Type[Model]], 
            branch_points_list: List[List[Tuple[float, float]]],
            branch_params: Union[List[float], float, int],
        ):
        self.model: Type[Model] = model
        self.dummy_points = branch_points_list[0]
        self.branches: List[Model] = [model(*pts) for pts in branch_points_list]
        self.param_model_dict: Dict[str, str] = param_model_dict
        self.branch_params = branch_params
        self.param_model: Dict[str, Model] = self._compute_param_model_at_x0(branch_params) if isinstance(branch_params, float) or isinstance(branch_params, int) else self._compute_param_model_custom_params(branch_params)


    def get_interpolation(self, value: float, boundary_condition: Optional[Tuple[float, float]] = None) -> Model:
        model = self.model(*self.dummy_points)
        model.reset_model({
            k: self.param_model[k].model()(value)
            for k in self.param_model
        })
        if boundary_condition is not None:
            y0 = model.model()(boundary_condition[0])
            params = model.parameters()
            params[model.offset_parameter()] += (boundary_condition[1] - y0)
            model.reset_model(params)
        return model
    
    def _plot_param_model_check(self, param: str, basename: str):
        if isinstance(self.branch_params, list):
            pts = [
                [x, self.param_model[param].model()(x)]
                for x in self.branch_params
            ]
        else:
            pts = [
                [model.model()(self.branch_params), self.param_model[param].model()(model.model()(self.branch_params))]
                for model in self.branches
            ]
        fig, ax = plt.subplots()
        ax.plot([p[0] for p in pts], [p[1] for p in pts], 'o')
        dx = (pts[-1][0] - pts[0][0]) / 100
        xs = [pts[0][0] + i*dx for i in range(0,101)]
        ax.plot([x for x in xs], [self.param_model[param].model()(x) for x in xs])
        fig.savefig(f"{basename}_{param}.png")
        

    def plot_param_model_check(self, basename: str):
        for param in self.param_model:
            self._plot_param_model_check(param=param, basename=basename)


    def _compute_param_model_custom_params(self, branch_params: List[float]) -> Dict[str, Model]:
        pfit = {}
        for param_name in self.branches[0].parameters():
            pfit[param_name] = [
                [branch_params[i], branch.parameters()[param_name]]
                for i, branch in enumerate(self.branches)
            ]
        param_model = {}
        for param_name, pts in pfit.items():
            param_model[param_name] = self.param_model_dict[param_name](*pts)
        return param_model
    

    def _compute_param_model_at_x0(self, x0: float) -> Dict[str, Model]:
        pfit = {}
        for param_name in self.branches[0].parameters():
            pfit[param_name] = [
                [branch.model()(x0), branch.parameters()[param_name]]
                for i, branch in enumerate(self.branches)
            ]
        param_model = {}
        for param_name, pts in pfit.items():
            param_model[param_name] = self.param_model_dict[param_name](*pts)
        return param_model
