from calendar import c
from control.buildcavity import Cavity_2Pi_3
from control.helper import calc_pfd_2pi_3_mode
from scipy.optimize import minimize
from pathlib import Path
import pandas as pd
SPEED_OF_LIGHT = 299792458
class Cavity_Optimizer:
    def __init__(self,opt_name="OPT01"):
        self.target_frequency = 2998.8  # MHz, target frequency for the cavity
        ####SET INITIAL PARAMETERS
        self.t=6/10;
        self.ia=2.7/10;self.ib=5.4/10;self.ts=0.6/10;self.br=7.5/10
        self.a=12.394588/10
        self.b=40.74236667298/10
        self.D=33.323602552132/10
        self.opt_name = opt_name
        self.save_dir = Path("result") / self.opt_name
        
        self.runrecords= []
        self.optrecords=[]
        self._opt_index=0
    def _new_opt_record_index(self):
        index= self._opt_index
        self._opt_index += 1
        return index
    def wave_length(self):
        return SPEED_OF_LIGHT / (self.target_frequency * 1e6)  # Convert MHz to Hz
    def cavity_2pi_3(self,b):
        ###beta<1 part
        index=self._new_opt_record_index()
        save_dir=self.save_dir / ("CAV_"+str(index).zfill(5))
        cav=Cavity_2Pi_3(self.t, self.ia, self.ib, self.ts, self.br, self.a, b, self.D, save_dir=save_dir)
        sfo,t35=cav.run_cavity_solver()
        pfd=calc_pfd_2pi_3_mode(t35)
        paramrecord=pd.DataFrame([[self.t, self.ia, self.ib, self.ts, self.br, self.a, b, self.D]],index=[index],columns=cav.param_columns)
        pfdrecord=pd.DataFrame([pfd], index=[index], columns=["Power factor density"])
        record=pd.concat([paramrecord, sfo, pfdrecord], axis=1)
        self.runrecords.append(record)
        record.to_csv(save_dir / f"cavity_{index}.csv", index=False)
        return record
    def objective_function(self, bs):
        result= self.cavity_2pi_3(bs[0])
        calculated_frequency=result.head(1)['Frequency']
        print(f"Calculated frequency: {calculated_frequency} MHz")
        return (calculated_frequency - self.target_frequency) ** 2
    def save_records(self):
        if len(self.records)==0:
            print("No records")
            return
        records_df = pd.concat(self.records)
        records_df.to_csv(self.save_dir / f"{self.opt_name}_records.csv")
                  
    def optimize_cavity(self, initial_guess):
        """
        Optimize the cavity parameters to achieve the target frequency.
        
        Parameters:
        initial_guess (list): Initial guess for the cavity parameters.
        
        Returns:
        result (OptimizeResult): The optimization result.
        """
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True, exist_ok=True)
        if any(self.save_dir.iterdir()):
            print(f"Warning: Directory {self.save_dir} is not empty. Previous records may be overwritten.")
        result = minimize(self.objective_function, initial_guess, method='BFGS',tol=1e-3,bounds=[(item*0.9, item*1.1) for item in initial_guess])
        runrecords= pd.concat(self.runrecords)
        runrecords.to_csv(self.save_dir / f"{self.opt_name}_run_records.csv", index=False)
        return result
    
if __name__ == "__main__":
    opt= Cavity_Optimizer(opt_name="OPT01")
    result=opt.optimize_cavity(initial_guess=[opt.b])
    print("Optimization Result:")
    print(result)