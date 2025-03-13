# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import pytest
import sys

from conftest import SAMPLES_PY_DIR, SAMPLES_CPP_DIR
from test_utils import run_sample

class TestVisualLanguageChat:
    @pytest.mark.vlm
    @pytest.mark.samples
    @pytest.mark.parametrize(
        "convert_model, download_test_content, questions",
        [
            pytest.param("llava-1.5-7b-hf", "monalisa.jpg", 'Who drew this painting?\nWhen did the painter live?'),
            pytest.param("llava-v1.6-mistral-7b-hf", "monalisa.jpg", 'Who drew this painting?\nWhen did the painter live?'),
            pytest.param("InternVL2-1B", "monalisa.jpg", 'Who drew this painting?\nWhen did the painter live?'),
            pytest.param("Qwen2-VL-2B-Instruct", "monalisa.jpg", 'Who drew this painting?\nWhen did the painter live?'),
            pytest.param("tiny-random-minicpmv-2_6", ("cat.png", "images"), 'What is unusual on this image?\nGo on.')
        ],
        indirect=["convert_model", "download_test_content"],
    )
    def test_sample_visual_language_chat(self, request, convert_model, download_test_content, questions):
        model_name = request.node.callspec.params['convert_model']
        
        # Test Python sample
        py_script = os.path.join(SAMPLES_PY_DIR, "visual_language_chat/visual_language_chat.py")
        py_command = [sys.executable, py_script, convert_model, download_test_content]
        py_result = run_sample(py_command, questions)

        # Test CPP sample
        cpp_sample = os.path.join(SAMPLES_CPP_DIR, 'visual_language_chat')
        cpp_command =[cpp_sample, convert_model, download_test_content]
        cpp_result = run_sample(cpp_command, questions)

        # Compare results
        if model_name != "Qwen2-VL-2B-Instruct": # "Skipping result comparison for Qwen2-VL-2B-Instruct due to CVS-164144"
            assert py_result.stdout == cpp_result.stdout, f"Results should match"

    @pytest.mark.vlm
    @pytest.mark.samples
    @pytest.mark.parametrize(
        "convert_model, questions",
        [
            pytest.param("tiny-random-minicpmv-2_6", 'Describe the images?'),
        ],
        indirect=["convert_model"],
    )
    @pytest.mark.parametrize("download_test_content", [("cat.png", "images")], indirect=True)
    @pytest.mark.parametrize("generate_test_content", [("lines.png", "images")], indirect=True)
    def test_sample_visual_language_chat_images(self, convert_model, download_test_content, generate_test_content, questions):
        # Test Python sample
        py_script = os.path.join(SAMPLES_PY_DIR, "visual_language_chat/visual_language_chat.py")
        py_command = [sys.executable, py_script, convert_model, os.path.dirname(generate_test_content)]
        py_result = run_sample(py_command, questions)

        # Test CPP sample
        cpp_sample = os.path.join(SAMPLES_CPP_DIR, 'visual_language_chat')
        cpp_command =[cpp_sample, convert_model, os.path.dirname(generate_test_content)]
        cpp_result = run_sample(cpp_command, questions)

        # Compare results
        assert py_result.stdout == cpp_result.stdout, f"Results should match"
