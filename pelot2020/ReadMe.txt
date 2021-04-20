//////////////////////  README for Extended Axon Modeling Project  /////////////////////////

Author: Brandon Thio
Last Updated: 12/10/2020

///////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////   Overview    ////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////
This file contains a description of the file structure of the code. Note that the mod files containing the ion channel mechanisms must 
be compiled using mknrndll after migrating the files to a different machine or after making any edits.
The resulting dll file must be stored in the directory in which the hoc files are stored. 
Note the file structure is for organizational purposes, and all the .m, .hoc, .dll, and .csv files need to be in the same directory to run properly.

All mechanisms for the Sundt et al. 2015, Tigerholm et al. 2014, Rattay and Aberham 1993, and Schild et al 1994/97 are located in the Mod folder.

///////////////////////////////////////////////////////////////////////////////////	
////////////////////////////////  Simulations   ///////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
There are three HOC files which complete different simulation tasks. These are:

	CV.hoc - runs conduction velocity test
	SD.hoc - runs strength duration task
	PairPulseTrue.hoc - runs recovery cycle task

All simulation tasks call cFiberBuilder.hoc and if using the tigerholm fiber, balanceTigerholm.hoc will be called.

///////////// cFiberBuilder.hoc ////////////////
cFiberBuilder.hoc creates a c-fiber model and takes in parameters associated with the fiber diameter, length, 
model type, temperature, segment density, and, if the fiber is a Schild fiber, a pair of flags for using Schild 94 or 97 parameters

model type		1: Sundt 2015
			2: Tigerholm 2014
			3: Rattay and Aberham 1993
			4: Schild 1997
			5: Schild 1994

Instantiation of the fiber can be seen in any of the simulation task hoc files.

///////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////  Matlab Scripts  //////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////

There is code to Batch the neuron code from matlab. Batch<task>.m is the general format of the files.
These files use call_neuron_MATLAB.m to interface with your machine's version of NEURON and run .hoc scripts.
Master.m runs all the different simulation tasks serially.