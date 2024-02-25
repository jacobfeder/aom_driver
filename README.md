# 2-Tone AOM driver
This custom acousto-optic modulator (AOM) driver PCB is designed for generating short light pulses with enhanced isolation and power stability compared to traditional AOM configurations.

![AOM PCB rendering](https://github.com/jacobfeder/aom_driver/blob/main/aom_driver.png)

# Background
When generating light pulses with an AOM, two parameters that you may care about are the isolation and power stability.

The isolation (usually expressed in dB) is defined as $10*\log_{10}(P_{on} / P_{off})$, where $P_{on}$ is the transmitted optical power with the AOM enabled, and $P_{off}$ is the transmitted optical power with the AOM disabled. A low isolation means that even when the AOM is disabled, there is significant light leakage through the AOM, which can be undesirable for certain applications.

Power stability is the change in transmitted optical power as a function of time or AOM duty cycle. The active area of an AOM that the optical beam passes through is made of a material whose optical index of refraction changes with strain (acoustic waves), producing the desired beam diffraction. However, other variables, such as temperature, can impact the index of refraction and, therefore, the pointing stability of the beam.

Many traditional AOM drivers are used as follows:
- The driver produces a single frequency which is toggled on and off, often with relatively low isolation.
- The optical power is switched between being primarily concentrated in the 0th order diffraction peak (AOM disabled, RF off) and the 1st order peak (AOM enabled, RF on).

This configuration produces two undesirable effects. First, drivers with low isolation (RF power $P_{on}/P_{off}$) can limit the optical isolation of the AOM due to parasitic driving of the AOM with RF leakage. Second, when switching the RF drive on/off, there is a change in RF power dissipation in the AOM crystal, inducing a temperature change. This temperature change reduces the beam pointing stability and produces power fluctuations as a function of time and switching duty cycle.

# Overview

The 2-Tone AOM driver greatly mitigates isolation and power stability issues. Whereas traditional AOM drivers rapidly switch between an RF signal being on or off, this driver rapidly switches between two different RF frequencies. The optical power diffracted by the AOM with low-frequency drive should ideally be fiber coupled into a single-mode fiber and then used in your down-stream application. The optical power diffracted by the AOM with the high-frequency "dummy" drive should be sent into a beam-dump. If the power of the two frequencies produced by this driver are properly calibrated, thermalization effects of the AOM crystal can be minimized because the RF power delivered to the crystal is equal for both frequencies. The driver can switch between these two frequencies with very high RF isolation such that the achievable AOM optical isolation will likely become limited by the physics of gaussian optics (see additional notes below).

# Specifications
- RF isolation ~90dB
- Both frequency outputs individually tunable from ~0dBm to <-30dBm (before amplifier, >30dBm after amplifier)
- Frequency range accessible with default VCO 140 - 250 MHz (much larger range possible by swapping VCO, see customization section)
- At the time of writing, cost is <$1000 for all parts
- Convenient DIN rail mounting
- TTL input switches between the two frequencies

# Principle of Operation
The driver consists of four main parts: two nearly-identical frequency synthesis sections, a fast RF switch to select the frequency, and an (off board) RF amplifier. The frequency synthesis sections begin with a voltage-controlled oscillator (VCO) that generates the initial RF signal (CVCO55xx). A fixed attenuator limits the maximum output power (PAT1220-C-x). Next, an amplifier increases the output power (GVA-81). A voltage-variable attenuator (VVA) allows the user to tune the output power of each frequency synthesis channel in real-time using a potentiometer in order to calibrate the system (RVA-3000R). A filter reduces some of the harmonics (RLP-xxx+). An RF switch (M3SWA-2-50DRB+) for each frequency synthesis channel toggles the frequency on/off before the final switch in order to increase isolation. This concludes the frequency synthesis sections. A final RF switch (M3SWA-2-50DRB+) selects the output frequency channel. The AOM driver output is intended to then be fed to an external RF amplifier.

# Required Parts
- The 2-tone AOM driver PCB (see aom_driver.csv for PCB BOM)
- +-15V DC power supply for the AOM driver PCB, recommend TODO
- RF amplifier, recommend [Minicircuits ZHL-03-5WF+](https://www.minicircuits.com/WebStore/dashboard.html?model=ZHL-03-5WF%2B)
- 24V DC power supply for the RF amplifier, recommend TODO

# Customization
The driver is designed to be easily customized. The critical components were chosen such that they can be swapped out with pin-pin compatible components with different characteristics.

### Frequency
The VCO can be substituted for nearly any member of the [Crystek CVCO55 series](https://www.crystek.com/home/vco/cvco55.aspx), which should accomodate a widge range of AOM drive frequencies. By default, the schematic is configured to output 150 MHz and 250 MHz. The VCO specified in the schematic has a range of 140 - 250 MHz. Changing the frequency in this range can be accomplished by configuring resistors $R_{5}$, $R_{6}$ for channel 1 and $R_{7}$, $R_{8}$ for channel 2. The VCO output frequency as a function of tuning voltage is given by the tuning curve in the [datasheet](https://www.crystek.com/specification/vco/CVCO55CW-0140-0250.pdf). The VCO tuning voltage is $10 \text{uA} * (R_5 + R_6)$ for channel 1, and $10 \text{uA} * (R_7 + R_8)$ for channel 2. For example, let's imagine you wanted an output frequency of 200 MHz on channel 1. The CVCO55CW-0140-0250 tuning curve shows that you would need a tuning voltage of 6 V. Then you would set $R_5 + R_6 = 6 \text{V} / 10 \text{uA} = 600 \text{kOhm}$. Similarly, resistors $R_{9}$ and $R_{10}$ set the VCO power supply voltages and can be substituted as needed according to $V_{CC} = 10 \text{uA} * R_{9}$ and $V_{CC} = 10 \text{uA} * R_{10}$. When changing the drive frequency, filters FL1 and FL2 should potentially be changed in order to accomodate the new frequency. They should be chosen such that the primary frequency is minimally attenuated, but harmonics are maximally attenuated. However, attenuating harmonics may not have a significant impact on the performance for reasons explained in the additional notes section.

### Power
The final RF output power of the system is impossible to predict precisely due to the tolerance stackup of all the components, which is why the board contains a potentiometer for individually tuning the output power of each frequency synthesis channel as well as a power-limiting fixed attenuator. The driver PCB should be capable of outputting a maximum power of >0dBm. The [Minicircuits ZHL-03-5WF+](https://www.minicircuits.com/WebStore/dashboard.html?model=ZHL-03-5WF%2B) has a gain of >30dB, so the final output power that can be achieved before the AOM is in excess of 1W. AOMs (and power amplifiers) can be damaged by too much input power. For this reason, a fixed attenuator PAT1220-C-x is included (U7 and U8) to limit the driver PCB maximum output power. Before connecting the driver PCB to the RF amplifier or AOM, the driver PCB output power should be measured. It is recommended to pick a specific PAT1220-C-x fixed attenuator for U7 and U8 in order to limit the maximum output power for your given RF amplifier and AOM such that no damage to either component is possible when the VVA poteniometer is tuned to output the maximum power from the driver PCB.

# Additional Notes
- The AOM driver system will cause the AOM to produce several optical beams at its output due to both AOM physics and RF design. When the low-frequency RF path is selected, it will produce 0th, 1st, 2nd, ..., nth order beams. The 1st order beam is the desired optical output and should go to the downstream application. All other 0th, 2nd, etc. order beams should be blocked or otherwise not coupled into the optical output. When the high frequency is selected, it will also produce 0th, 1st, 2nd, ..., nth order beams. All of these beams are "dummy" beams and should be blocked or otherwise not coupled into the downstream application. It is important to use the 1st order low-frequency beam for your application, as it will have minimal interference from RF drive harmonics.
- While the AOM driver has very high RF isolation, achieving high optical isolation requires additional careful attention to detail with optical design. I would recommend fiber coupling the 1st order low-frequency beam after the AOM for best performance.
- If all beams except the low-frequency 1st order beam are sufficiently blocked, the optical isolation will likely become limited by gaussian optics considerations. A beam of light entering the AOM will always have some finite divergence. After exiting the AOM, many beams are generated as explained above. These undesired beams will always have some degree of coupling into the desired output path due to their finite divergence, limiting the total optical isolation. A script is provided (TODO) to help with calculating the optical isolation. There is a somewhat intuitive explanation for this optics-limited isolation by consdering the tradeoff between isolation, rise-time, and AOM RF bandwidth. Getting a faster rise-time requires a smaller optical spot size on the AOM crystal, which requires a higher beam divergence. Higher divergence results in reduced isolation as explained above. Higher AOM RF bandwidth allows the primary and "dummy" beams to be separated by a larger angle, which increases their isolation. Therefore, it is important to consider the RF bandwidth when selecting an AOM.

Feel free to email me if you have any questions at <jacobsfeder@gmail.com>.

# Acknowledgements
- This project would not have been possible without the help of Arron Campi at Gooch and Housego. He graciously provided his time and insight by helping me to understand AOM physics and limitations, as well as suggesting the idea of driving the AOM with multiple frequencies.
- Ben Soloway contributed the script that calculates optical isolation, and provided comic relief in addition to being my scientific partner in crime.
- The Awschalom Lab at UChicago and the NSF provided financial support.
