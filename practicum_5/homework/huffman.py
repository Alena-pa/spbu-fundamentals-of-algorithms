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
        self.char = None

    def encode(self, sequence: list[Any]) -> str:
        nodes = []
        freqencies = {}
        counter = 0

        #counting number of occurrences of a letter in a word
        for char in sequence:
            if char not in freqencies:
                freqencies[char] = 0
            freqencies[char] += 1

        for char, freq in freqencies.items():
            heapq.heappush(nodes, (freq, counter, char, None, None))
            counter += 1

        #building huffman tree
        while len(nodes) > 1:
            left = heapq.heappop(nodes)
            right = heapq.heappop(nodes)
            parent = (left[0] + right[0], counter, None, left, right)
            counter += 1
            heapq.heappush(nodes, parent)

        root = nodes[0]
        codes = {}

        #encoding
        def build_codes(node, current_code=""):
            freq, _, char, left, right = node
            if left is None and right is None:
                codes[char] = current_code
                return
            build_codes(left, current_code + "0")
            build_codes(right, current_code + "1")

        build_codes(root)
        self.char = codes
        encoded = "".join(codes[char] for char in sequence)
        return encoded

    def decode(self, encoded_sequence: str) -> list[Any]:
        curr_code = ""
        decoded = []

        code_to_char = {value: key for key, value in self.char.items()}
        for char in encoded_sequence:
            curr_code += char
            if curr_code in code_to_char:
                decoded.append(code_to_char[curr_code])
                curr_code = ""
        return decoded


class LossyCompression:
    def __init__(self) -> None:
        self.levels = None
        self.min_value = None
        self.max_value = None
        self.huffman = HuffmanCoding()
        self.centers = None

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min_value = time_series.min()
        self.max_value = time_series.max()
        self.levels = len(time_series)
        intervals = np.linspace(self.min_value, self.max_value, self.levels + 1)

        self.centers = []
        for i in range(self.levels):
            self.centers.append((intervals[i] + intervals[i + 1]) / 2)

        quantized = []
        for i in time_series:
            index_of_value = np.searchsorted(intervals, i)
            if index_of_value == self.levels:
                index_of_value -= 1
            quantized.append(index_of_value)

        encoded = self.huffman.encode(quantized)
        return encoded

    def decompress(self, bits: str) -> NDArrayFloat:
        quantized = self.huffman.decode(bits)

        decompressed = [self.centers[index] for index in quantized]
        return np.array(decompressed)

if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)
    compression_ratio = (len(ts) * 32 * 8) / len(bits)
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")