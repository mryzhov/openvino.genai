# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import pytest
import sys

from conftest import TEST_FILES, SAMPLES_PY_DIR, SAMPLES_CPP_DIR
from test_utils import run_sample

class TestVisualLanguageChat:
    @pytest.mark.vlm
    @pytest.mark.samples
    @pytest.mark.parametrize(
        "convert_model, sample_args",
        [
            pytest.param("llava-1.5-7b-hf", 'Who drew this painting?\nWhen did the painter live?'),
            pytest.param("llava-v1.6-mistral-7b-hf", 'Who drew this painting?\nWhen did the painter live?'),
        ],
        indirect=["convert_model"],
    )
    @pytest.mark.parametrize("download_test_content", [TEST_FILES["monalisa.jpg"]], indirect=True)
    def test_sample_visual_language_chat(self, convert_model, download_test_content, sample_args):
        # Test Python sample
        py_script = os.path.join(SAMPLES_PY_DIR, "visual_language_chat/visual_language_chat.py")
        py_command = [sys.executable, py_script, convert_model, download_test_content, '<<<', f'"${sample_args}"']
        py_result = run_sample(py_command)

        # Test CPP sample
        cpp_sample = os.path.join(SAMPLES_CPP_DIR, 'visual_language_chat')
        cpp_command =[cpp_sample, convert_model, download_test_content, '<<<', f'"${sample_args}"']
        cpp_result = run_sample(cpp_command)

        # Compare results
        assert py_result.stdout == cpp_result.stdout, f"Results should match"
