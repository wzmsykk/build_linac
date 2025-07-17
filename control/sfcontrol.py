
from pathlib import Path
import os,shutil
from tkinter import NO
import numpy as np
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
            cmd_line=str(self.superfish_dir / app_name)+" "+str(control)+" "+str(filepath)
            print(f"Superfish command: {cmd_line}")
            os.system(cmd_line)
            print(f"Input File Path: {filepath}")
            SF7RESULT= "OUTSF7.TXT"
            with open(SF7RESULT, 'r') as SF7RESULT:
                lines = SF7RESULT.readlines()
                for line in lines:
                    if "Interpolated" in line:
                        outname = Path(line.split()[-1].strip()[:-1])
                        print(f"Output file found: {outname}")
                        break
            return outname if outname.exists() else None
        except Exception as e:
            print(f"Error starting Superfish: {e}")
            return None
sfc=SFControl()
class SFDataProcessor:
    def __init__(self):
        pass
    def create_sf7_input(self):
        pass
    def process_tbl_data(self, tbl_file):
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
        return df, title, unit
            
            
    def postprocess_T35_data(self, t35_file, start_point=(0,0),end_point=(0,0),intp_points=None):
        """Post-process T35 data to extract relevant fields."""
        # Should provide the path to the T35 file and interpolate line
        if not t35_file.exists():
            raise FileNotFoundError(f"T35 file {t35_file} does not exist.")
        if intp_points is None:
            raise ValueError("Interpolation points must be provided.")
        with tempfile.TemporaryDirectory() as tempdir:
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
            df, title, unit=self.process_tbl_data(resultfile)   
            os.chdir(original_cwd)
        return df, title, unit
            
if __name__ == "__main__":
    ssfdpc=SFDataProcessor()
    Path("temp").mkdir(exist_ok=True)
    testfieldpath=Path("./test/fieldresult/1CELL.T35").absolute()
    testfieldpath2=Path("./test/cavinputtest/CAVITY_INPUT.T35").absolute()
    controlfilepath=Path("./test/fieldresult/cmd.in7").absolute()
    df, title, unit=ssfdpc.postprocess_T35_data(testfieldpath,start_point=(1.666180128,0.0),end_point=(1.666180128,1.2394588),intp_points=1001)
    print(df)
