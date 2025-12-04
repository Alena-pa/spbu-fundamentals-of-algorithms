from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.root = None

    def encode(self, sequence: list[Any]) -> str:
        encoded = {}
        nodes = []
        frequencies = {}
        heap = []
        counter = 0

        for char in sequence:
            if char not in frequencies:
                freq = sequence.count(char)
                frequencies[char] = freq
                nodes.append((char, freq))

        for char, freq in nodes:
            heapq.heappush(heap, (freq, counter, char))
            counter += 1

        while len(heap) > 0:
            leftChar = heapq.heappop(heap)
            rightChar = heapq.heappop(heap)
            new_node = (leftChar[2], rightChar[2])
            heapq.heappush(heap, (leftChar[0] + rightChar[0], counter, new_node))
            counter += 1

        self.root = heap[0][2]
        self.codes = {}

        def build_codes(node, current_code):
            if not isinstance(node, tuple):
                self.codes[node] = current_code
                return
            build_codes(node, current_code + '0')
            build_codes(node, current_code + '1')

        build_codes(self.root, "")

        encoded = "".join(self.codes[ch] for ch in sequence)
        return encoded


        

    def decode(self, encoded_sequence: str) -> list[Any]:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


class LossyCompression:
    def __init__(self) -> None:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def compress(self, time_series: NDArrayFloat) -> str:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def decompress(self, bits: str) -> NDArrayFloat:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

