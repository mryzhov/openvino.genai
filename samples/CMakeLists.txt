# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#

add_subdirectory(cpp/beam_search_causal_lm)
add_subdirectory(cpp/benchmark_genai)
add_subdirectory(cpp/chat_sample)
add_subdirectory(cpp/text_generation)
add_subdirectory(cpp/lora_greedy_causal_lm)
add_subdirectory(cpp/multinomial_causal_lm)
add_subdirectory(cpp/prompt_lookup_decoding_lm)
add_subdirectory(cpp/speculative_decoding_lm)
add_subdirectory(cpp/image_generation)
add_subdirectory(cpp/visual_language_chat)
add_subdirectory(cpp/whisper_speech_recognition)

install(FILES
        deployment-requirements.txt
        export-requirements.txt
        requirements.txt
    DESTINATION samples
    COMPONENT cpp_samples_genai)

install(DIRECTORY
            cpp/beam_search_causal_lm
            cpp/benchmark_genai
            cpp/chat_sample
            cpp/text_generation
            cpp/image_generation
            cpp/lora_greedy_causal_lm
            cpp/multinomial_causal_lm
            # Don't install prompt_lookup_decoding_lm because it doesn't use openvino_genai library and is not verified yet.
            cpp/speculative_decoding_lm
            cpp/visual_language_chat
            cpp/whisper_speech_recognition
        DESTINATION samples/cpp COMPONENT cpp_samples_genai)

install(DIRECTORY
            python/beam_search_causal_lm
            python/benchmark_genai
            python/chat_sample
            python/text_generation
            python/image_generation
            python/multinomial_causal_lm
            python/speculative_decoding_lm
            python/visual_language_chat
            python/whisper_speech_recognition
        DESTINATION samples/python COMPONENT cpp_samples_genai
        USE_SOURCE_PERMISSIONS)
