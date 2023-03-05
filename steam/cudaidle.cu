/*
Keep P2 state permanently

This utility helps overclocked systems not to enter P0 state and crash.

usage: cudaidle [device=N]

Contact petri33 @ setiathome

nvcc -O3 -I ./cuda-samples/Common cudaidle.cu -o cudaidle
*/

#include <stdio.h>
#include <unistd.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>

// a variable in GPU memory
__device__ int i;

__global__ void kernel(int val)
{
	i = 0;
}

int main(int argc, char **argv)
{
	int devID;
	cudaDeviceProp props;

	// This will pick selected or the best possible CUDA capable device
	devID = findCudaDevice(argc, (const char **)argv);

	//Get GPU information
	checkCudaErrors(cudaGetDevice(&devID));
	checkCudaErrors(cudaGetDeviceProperties(&props, devID));
	printf("Device %d: \"%s\" with Compute %d.%d capability\n", devID, props.name, props.major, props.minor);
	printf("Keep in P2 state enabled.\nCreated 2018 by petri33 @ setiathome\n\n");

	//minimal Kernel configuration
	dim3 dimGrid(1);
	dim3 dimBlock(1);

	unsigned int microseconds = 100000; // 0.1 seconds

	for(;;)
	{
		// run 10 times a second, negligible performance hit
		kernel<<<dimGrid, dimBlock>>>(0);
		usleep(microseconds);
	}

	return EXIT_SUCCESS;
}
