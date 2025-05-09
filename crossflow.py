from dataclasses import dataclass
from typing import Optional
import numpy as np
from sympy import symbols, solve, exp
from scipy.optimize import fsolve

@dataclass
class ThermoFluidProperties: 
    """Metaparameters of Water"""

    cmin: Optional[float] = None
    cr: Optional[float] = None
    
    water_flow_rate_L_min: float = 2.10  # L/min
    water_vol_flow_rate: Optional[float] = None
    water_density: float = 1000.0 
    water_mass_flow_rate: Optional[float] = None
    water_specific_heat: float = 4.18  # kJ/kgK
    
    # Temperature changes
    T_hot_in: float = 47.4  # Water inlet temp
    T_hot_out: float = 46.4  # Water outlet temp
    T_cold_in: float = 25.5  # Air inlet temp
    T_cold_out: float = 43.0  # Air outlet temp
    
    # Delta Temp calculation
    deltaT1: float = T_hot_in - T_cold_out  # deltT at one end
    deltaT2: float = T_hot_out - T_cold_in  # deltT at other end
    water_temp_change: float = T_hot_in - T_hot_out  # Changed
    air_temp_change: float = T_cold_out - T_cold_in  
    
    """Metaparamters of Air"""
    air_specific_heat: float = 1.005  # kJ/kgK
    air_mass_flow_rate: Optional[float] = None
    
    def calculate_duty(self) -> float:
        """Calculate heat duty (Q) in Watts"""
        Q = (self.water_mass_flow_rate * 
             self.water_specific_heat * 
             self.water_temp_change * 1000)  # Convert to Watts
        return Q
    
    def calculate_water_mass_flow(self) -> float:
        """Calculate water mass flow rate in kg/s"""
        self.water_vol_flow_rate = self.water_flow_rate_L_min*(1/1000)*(1/60) # convert to cubic meter/s
        self.water_mass_flow_rate = self.water_vol_flow_rate * self.water_density # Produces mass flow rate in kg/s
        return  self.water_mass_flow_rate 
    
    def calculate_air_mass_flow(self) -> float:
        """Calculate air mass flow rate in kg/s"""
        Q = self.calculate_duty()
        self.air_mass_flow_rate = Q / (self.air_specific_heat * self.air_temp_change * 1000)  # Added *1000 to match units
        return self.air_mass_flow_rate
    
    #Run this first to access cmin and cr values 
    def calculate_heat_capacity_rates(self) -> (float, float):
        """Calculate hot and cold heat capacity rates (Ch, Cc)"""
        C_h = self.water_mass_flow_rate * self.water_specific_heat * 1000  # Convert to W/K
        C_c = self.air_mass_flow_rate * self.air_specific_heat * 1000     # Convert to W/K
        self.cr = C_c/C_h
        if C_h <= C_c:
            self.cmin = C_h
        else:
            self.cmin = C_c
        return C_h, C_c
    
    # def calculate_capacity_ratio(self) -> float:
    #     """Calculate heat capacity ratio (Cr)"""
    #     C_h, C_c = self.calculate_heat_capacity_rates()
    #     return C_c / C_h  # Returns 0.098
    
    def calculate_actual_heat_transfer(self) -> float:
        """Calculate actual heat transfer rate (q_actual) in Watts"""
        C_h, _ =self.calculate_heat_capacity_rates()
        return C_h*self.water_temp_change  
    
    def calculate_max_heat_transfer(self) -> float:
        """Calculate maximum possible heat transfer rate (q_max) in Watts"""
        _, C_c = self.calculate_heat_capacity_rates()
        return self.cmin * (self.T_hot_in - self.T_cold_in)  # Using Cmin instead of C_c
    
    def calculate_effectiveness(self) -> float:
        """Calculate heat exchanger effectiveness (ε)"""
        q_actual = self.calculate_actual_heat_transfer()
        q_max = self.calculate_max_heat_transfer()
        return q_actual / q_max  
    
    def calculate_NTU_from_effectiveness(self) -> float:
        """
        solves for NTU using the effectiveness equation:
        ep = 1 - exp[(1/Cr)(NTU)^0.22{exp[-Cr(NTU)^0.78] - 1}]
        """
        def effectiveness_equation(NTU):
            # Known values
            eps = self.calculate_effectiveness()  # Get effectiveness
            cr = self.cr                         # Get capacity ratio
            
            # The equation rearranged to equal zero
            return (1 - eps) - np.exp((1/cr) * NTU**0.22 * (np.exp(-cr * NTU**0.78) - 1))
        
        ntu_guess = 1.0
        ntu_solution = fsolve(effectiveness_equation, ntu_guess)[0]
        return ntu_solution

    def calculate_fin_efficiency(self) -> float:
        """
        Calculate individual fin efficiency for straight, rectangular fins
        
        Returns:
            float: Fin efficiency (η_f)
        """
        # Given constants
        h = 100.0  # W/(m^2·K)
        k = 401.0  # W/(m·K)
        w = 16.1/1000  # Convert mm to m
        t = 0.11/1000  # Convert mm to m
        L = 3.72/1000  # Convert mm to m
        
       
        P = 2*w + 2*t  
        A_c = w*t      
        L_c = L + t/2  
        
       
        m = np.sqrt((h*P)/(k*A_c))  
        
        # Calculate fin efficiency
        eta_f = np.tanh(m*L_c)/(m*L_c)  
        
        return eta_f

if __name__=="__main__":
    instance1 = ThermoFluidProperties()

    
    water_mass = instance1.calculate_water_mass_flow()
    print(f"\nWater mass flow rate: {water_mass} kg/s")
    
    
    duty = instance1.calculate_duty()
    print(f"Heat duty: {duty} W")
    
   
    air_mass = instance1.calculate_air_mass_flow()
    print(f"Air mass flow rate: {air_mass} kg/s")
    
    
    C_h, C_c = instance1.calculate_heat_capacity_rates()
    print(f"\nHeat capacity rates:")
    print(f"C_h (hot fluid): {C_h} W/K")
    print(f"C_c (cold fluid): {C_c} W/K")
    
    
    q_actual = instance1.calculate_actual_heat_transfer()
    print(f"\nActual heat transfer rate: {q_actual} W")
    
    
    q_max = instance1.calculate_max_heat_transfer()
    print(f"Maximum heat transfer rate: {q_max} W")
    
    
    effectiveness = instance1.calculate_effectiveness()
    print(f"\nHeat exchanger effectiveness: {effectiveness}")
    
    ntu = instance1.calculate_NTU_from_effectiveness()
    print(f"\nNumber of Transfer Units (NTU): {ntu:.3f}")
    print(f"The Thermal Conductance(UA) is {ntu*C_c} W/K")

    fin_efficiency = instance1.calculate_fin_efficiency()
    print(f"\nFin efficiency (η_f): {fin_efficiency:.3f}")

