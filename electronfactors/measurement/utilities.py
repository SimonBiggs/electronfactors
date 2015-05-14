# Copyright (C) 2015 Simon Biggs
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# http://www.gnu.org/licenses/.

import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import pylab

from scipy.interpolate import RectBivariateSpline


def energy_to_reference_depth(input_energy):
    valid_energies = np.array([6, 9, 12, 15, 18])
    if not(input_energy in valid_energies):
        raise Exception("Not valid energy")

    reference = input_energy == valid_energies
    depths = np.array([13, 20, 25, 27, 30])
    depth = depths[reference]

    return depth


def energy_to_R50(input_energy):
    valid_energies = np.array([6, 9, 12, 15, 18])
    if not(input_energy in valid_energies):
        raise Exception("Not valid energy")

    reference = input_energy == valid_energies
    R50s = np.array([24.1, 35.1, 46.2, 58.8, 70.8])
    R50 = R50s[reference]

    return R50


def TRS398_table7():
    table = dict()
    table['R50'] = [
        1.0, 1.4, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5,
        6.0, 7.0, 8.0, 10.0, 13.0, 16.0, 20.0
    ]
    table['depth/R50'] = [
        0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35,
        0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75,
        0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15,
        1.20
    ]
    table['contents'] = [
        [1.076, 1.060, 1.042, 1.030, 1.020, 1.012, 1.004, 0.997, 0.991, 0.986,
         0.980, 0.971, 0.963, 0.950, 0.935, 0.924, 0.914],
        [1.078, 1.061, 1.044, 1.032, 1.022, 1.014, 1.006, 1.000, 0.994, 0.988,
         0.983, 0.974, 0.965, 0.952, 0.937, 0.926, 0.916],
        [1.080, 1.064, 1.047, 1.036, 1.026, 1.018, 1.010, 1.004, 0.998, 0.992,
         0.987, 0.978, 0.970, 0.957, 0.942, 0.931, 0.920],
        [1.083, 1.067, 1.050, 1.039, 1.030, 1.022, 1.014, 1.008, 1.002, 0.997,
         0.992, 0.983, 0.975, 0.961, 0.946, 0.935, 0.924],
        [1.085, 1.070, 1.053, 1.043, 1.034, 1.026, 1.019, 1.012, 1.006, 1.001,
         0.996, 0.987, 0.979, 0.966, 0.951, 0.940, 0.929],
        [1.088, 1.073, 1.057, 1.046, 1.037, 1.030, 1.023, 1.017, 1.011, 1.006,
         1.001, 0.992, 0.984, 0.971, 0.956, 0.945, 0.933],
        [1.091, 1.076, 1.060, 1.050, 1.041, 1.034, 1.027, 1.021, 1.016, 1.010,
         1.006, 0.997, 0.989, 0.976, 0.961, 0.950, 0.938],
        [1.093, 1.079, 1.064, 1.054, 1.045, 1.038, 1.032, 1.026, 1.020, 1.015,
         1.011, 1.002, 0.995, 0.982, 0.966, 0.955, 0.943],
        [1.096, 1.082, 1.067, 1.058, 1.049, 1.042, 1.036, 1.030, 1.025, 1.020,
         1.016, 1.007, 1.000, 0.987, 0.972, 0.960, 0.948],
        [1.099, 1.085, 1.071, 1.062, 1.054, 1.047, 1.041, 1.035, 1.030, 1.025,
         1.021, 1.013, 1.006, 0.993, 0.978, 0.966, 0.953],
        [1.102, 1.089, 1.075, 1.066, 1.058, 1.051, 1.046, 1.040, 1.035, 1.031,
         1.027, 1.019, 1.012, 0.999, 0.984, 0.971, 0.959],
        [1.105, 1.092, 1.078, 1.070, 1.062, 1.056, 1.051, 1.045, 1.041, 1.036,
         1.032, 1.025, 1.018, 1.005, 0.990, 0.977, 0.964],
        [1.108, 1.095, 1.082, 1.074, 1.067, 1.061, 1.056, 1.051, 1.046, 1.042,
         1.038, 1.031, 1.024, 1.012, 0.996, 0.984, 0.970],
        [1.111, 1.099, 1.086, 1.078, 1.072, 1.066, 1.061, 1.056, 1.052, 1.048,
         1.044, 1.037, 1.030, 1.018, 1.003, 0.990, 0.976],
        [1.114, 1.102, 1.090, 1.082, 1.076, 1.071, 1.066, 1.062, 1.058, 1.054,
         1.050, 1.043, 1.037, 1.025, 1.010, 0.997, 0.983],
        [1.117, 1.105, 1.094, 1.087, 1.081, 1.076, 1.072, 1.067, 1.064, 1.060,
         1.057, 1.050, 1.044, 1.033, 1.017, 1.004, 0.989],
        [1.120, 1.109, 1.098, 1.091, 1.086, 1.081, 1.077, 1.073, 1.070, 1.066,
         1.063, 1.057, 1.051, 1.040, 1.025, 1.012, 0.996],
        [1.123, 1.112, 1.102, 1.096, 1.091, 1.087, 1.083, 1.080, 1.076, 1.073,
         1.070, 1.064, 1.059, 1.048, 1.033, 1.019, 1.004],
        [1.126, 1.116, 1.107, 1.101, 1.096, 1.092, 1.089, 1.086, 1.083, 1.080,
         1.077, 1.072, 1.067, 1.056, 1.041, 1.028, 1.011],
        [1.129, 1.120, 1.111, 1.106, 1.102, 1.098, 1.095, 1.092, 1.090, 1.087,
         1.085, 1.080, 1.075, 1.065, 1.050, 1.036, 1.019],
        [1.132, 1.124, 1.115, 1.111, 1.107, 1.104, 1.101, 1.099, 1.097, 1.095,
         1.092, 1.088, 1.083, 1.074, 1.059, 1.045, 1.028],
        [1.136, 1.127, 1.120, 1.116, 1.113, 1.110, 1.108, 1.106, 1.104, 1.102,
         1.100, 1.096, 1.092, 1.083, 1.069, 1.055, 1.037],
        [1.139, 1.131, 1.125, 1.121, 1.118, 1.116, 1.115, 1.113, 1.112, 1.110,
         1.109, 1.105, 1.102, 1.093, 1.079, 1.065, 1.046],
        [1.142, 1.135, 1.129, 1.126, 1.124, 1.123, 1.122, 1.120, 1.119, 1.118,
         1.117, 1.114, 1.111, 1.104, 1.090, 1.075, 1.056],
        [1.146, 1.139, 1.134, 1.132, 1.130, 1.129, 1.129, 1.128, 1.128, 1.127,
         1.126, 1.124, 1.121, 1.115, 1.101, 1.086, 1.066]
    ]

    return table


def find_stop_power(**kwargs):
    data = TRS398_table7()
    stop_power_interp = RectBivariateSpline(
        np.array(data['depth/R50']),
        np.array(data['R50']),
        np.array(data['contents'])
    )

    energy = kwargs['energy']
    depth_mm = np.array(kwargs['depth'])
    depth_cm = depth_mm / 10

    R50_mm = energy_to_R50(energy)
    R50_cm = R50_mm / 10

    depth_over_R50 = depth_cm / R50_cm
    stop_power = np.ravel(stop_power_interp.ev(depth_over_R50, R50_cm))

    return stop_power


def calc_and_display(**kwargs):
    depth = np.array(kwargs['depth'])
    ionisation = np.array(kwargs['ionisation'])
    reference = kwargs['reference']
    energy = kwargs['energy']

    reference_depth = energy_to_reference_depth(energy)
    reference_stop_power = find_stop_power(
        energy=energy, depth=reference_depth)

    if len(ionisation) == 1:
        field_stop_power = find_stop_power(
            energy=energy, depth=depth)
        stop_power_ratio = field_stop_power / reference_stop_power

        factor = ionisation / reference * stop_power_ratio

    else:
        field_stop_powers = find_stop_power(energy=energy, depth=depth)
        stop_ratio_corrected = field_stop_powers * ionisation

        plt.scatter(depth, stop_ratio_corrected)
        plt.ylabel('Stopping power ratio corrected')
        plt.xlabel('Depth (mm)')
        plt.title('Relative dose measurements')
        plt.show()

        index_of_max = np.argmax(stop_ratio_corrected)
        stop_power_ratio = (
            field_stop_powers[index_of_max] / reference_stop_power)

        factor = ionisation[index_of_max] / reference * stop_power_ratio

    print(
        "Cutout factor = %0.3f | %0.1f%%" %
        (factor, (factor - 1) * 100)
    )
    print(
        "Inverse factor = %0.3f | %0.1f%%" %
        (1/factor, (1/factor - 1) * 100)
    )

    return factor


def initialise(**kwargs):
    reference = kwargs['reference']
    energy = kwargs['energy']
    key = kwargs['key']
    data = kwargs['data']

    data[key] = dict()

    data[key]['depth'] = []
    data[key]['ionisation'] = []
    data[key]['reference'] = reference
    data[key]['energy'] = energy

    return data


def new_reading(**kwargs):
    data = kwargs['data']
    key = kwargs['key']
    ionisation = kwargs['ionisation']
    depth = kwargs['depth']

    data[key]['depth'].append(depth)
    data[key]['ionisation'].append(np.mean(ionisation))

    return data
