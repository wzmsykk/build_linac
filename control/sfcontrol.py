
from pathlib import Path
import os,shutil
import pandas as pd
import tempfile


class SFControl:
    def __init__(self, sf_dir=r"C:\LANL"):
        self.superfish_dir = Path(sf_dir)
        
    def start_SF7(self,inputfile="",controlfile=""):
        app_name = "SF7.EXE"
        
        try:
            filepath=Path(inputfile)
            control=Path(controlfile)
            print(f"Start SF7 Field Interpolation with input file: {inputfile} and control file: {controlfile}")
            cmd_line=str(self.superfish_dir / app_name)+" "+str(control)+" "+str(filepath)
            
            # print(f"SF7 Input File Path: {filepath}")
            print(f"SF7 command: {cmd_line}")
            os.system(cmd_line)
            SF7RESULT= "OUTSF7.TXT"
            with open(SF7RESULT, 'r') as fp:
                print(f"Opened SF7 output File: {SF7RESULT}")
                lines = fp.readlines()
                for line in lines:
                    if "Interpolated" in line:
                        outname = Path(line.split()[-1].strip()[:-1])
                        print(f"Output filename found in {SF7RESULT}: {outname}")
                        break
        except Exception as e:
            print(f"Error starting SF7: {e}")
            return None
        if outname.exists():
            print(f"Created Output file: {outname.absolute()}.")
            print("SF7 Field Interpolation Done.\n")
            return outname
        else:
            raise FileNotFoundError(f"Output file {outname} does not exist.")
    def start_AUTOFISH(self, inputfile=""):
        app_name = "AUTOFISH.EXE"
        try:
            filepath=Path(inputfile)
            print(f"Start AUTOFISH Solver with input file: {inputfile}")
            cmd_line=str(self.superfish_dir / app_name)+" "+str(filepath)
            print(f"AUTOFISH command: {cmd_line}")
            os.system(cmd_line)
            AFRESULT= filepath.with_suffix('.SFO')
            AFRESULT2= filepath.with_suffix('.T35')
        except Exception as e:
            print(f"Error starting AUTOFISH: {e}")
            return None
        if AFRESULT.exists():
                print(f"Created Output file: {AFRESULT.absolute()}.")
                print(f"Created Output file: {AFRESULT2.absolute()}.")
                print("AUTOFISH Solver Done.\n")
                return AFRESULT   
        else:
            raise FileNotFoundError(f"Output file {AFRESULT} does not exist.")
sfc=SFControl()
class SFDataProcessor:
    def __init__(self):
        Path("temp").mkdir(exist_ok=True)
    def create_sf7_input(self):
        pass
    def process_TBL_data(self, tbl_file):
        with open(tbl_file, 'r') as file:
            lines = file.readlines()
            found_data_start=False
            for i, line in enumerate(lines):
                if not found_data_start and "Data" in line:
                    start_index = i + 3
                    print(f"Start index: {start_index}")
                    found_data_start = True
                if "EndData" in line:
                    end_index = i
                    print(f"End index: {end_index}")
                    break
            data_lines = lines[start_index:end_index]
            data_lines = [line.strip().split() for line in data_lines if line.strip()]
            title = lines[start_index-2][1:].strip().split()
            unit= lines[start_index-1][1:].strip().split()
            df=pd.DataFrame(data_lines, columns=title)
        return df, unit
    def process_SFO_data(self, sfo_file):
        with open(sfo_file, 'r') as file:
            lines = file.readlines()
            start_search= False
            for i, line in enumerate(lines):
                if not start_search and "Superfish output summary for problem description:" in line:
                    start_search=True
                if start_search:
                    if "Frequency" in line:
                        frequency = float(line.strip().split()[2])  ### MHz
                    if "Shunt impedance" in line:
                        shunt_impedance = float(line.strip().split()[6])  ### MOhm
                        q = float(line.strip().split()[2])  ### MOhm
                    if "r/Q" in line:
                        r_over_q = float(line.strip().split()[2]) ### Ohm
                    if "Z*T*T" in line:
                        ztt = float(line.strip().split()[6]) ## MOhm
                    if "Power dissipation" in line:
                        loss = float(line.strip().split()[3])  ### W
        result = [frequency, shunt_impedance, q, r_over_q, ztt, loss]
        title = ["Frequency", "Shunt Impedance", "Q", "R/Q", "Z*T*T", "Power Dissipation"]
        unit = ["MHz", "MOhm", "MOhm", "Ohm", "MOhm", "W"]
        df= pd.DataFrame([result], columns=title)
        return df,unit
        pass
            
    def postprocess_T35_data(self, t35_file, start_point=(0,0),end_point=(0,0),intp_points=None):
        """Post-process T35 data to extract relevant fields."""
        # Should provide the path to the T35 file and interpolate line
        if not t35_file.exists():
            raise FileNotFoundError(f"T35 file {t35_file} does not exist.")
        if intp_points is None:
            raise ValueError("Interpolation points must be provided.")
        with tempfile.TemporaryDirectory(dir="temp") as tempdir:
            original_cwd = os.getcwd()
            os.chdir(Path(tempdir))
            tempin=shutil.copy(t35_file, tempdir)

            ####CREATE A CONTROL FILE FOR SF7
            ctrl_file= Path("CTRL.IN7")
            with open(ctrl_file, 'w') as fp:
                fp.write('Line	Plot\n')
                fp.write(f'{start_point[0]}\t{start_point[1]}\t{end_point[0]}\t{end_point[1]}\n')
                fp.write(f'{intp_points}\n')
                fp.write('End\n')
            resultfile=sfc.start_SF7(inputfile=tempin,controlfile=ctrl_file)
            df, unit=self.process_TBL_data(resultfile)   
            os.chdir(original_cwd)
        return df, unit
            
if __name__ == "__main__":
    ssfdpc=SFDataProcessor()
    Path("temp").mkdir(exist_ok=True)
    testfieldpath=Path("./test/field_result_data/1CELL.T35").absolute()
    testfieldpath2=Path("./test/cavity_input_data/CAVITY_INPUT.T35").absolute()
    afinput= Path("./test/cavity_input_data/CAVITY_INPUT.af").absolute()
    controlfilepath=Path("./test/field_result_data/cmd.in7").absolute()
    sfopath=Path("./test/cavity_input_data/CAVITY_INPUT.SFO").absolute()
    df, unit=ssfdpc.postprocess_T35_data(testfieldpath,start_point=(1.666180128,0.0),end_point=(1.666180128,1.2394588),intp_points=1001)
    print(df)
    df,unit=ssfdpc.process_SFO_data(sfopath)
    print(df)
    with tempfile.TemporaryDirectory(dir="temp") as tempdir:
        original_cwd = os.getcwd()
        os.chdir(Path(tempdir))
        tempin=shutil.copy(afinput, tempdir)
        result=sfc.start_AUTOFISH(inputfile=tempin)
        assert result.exists()
        print(f"AF Result file: {result}")
        df, unit=ssfdpc.process_SFO_data(result)
        print(df)
        os.chdir(original_cwd)
