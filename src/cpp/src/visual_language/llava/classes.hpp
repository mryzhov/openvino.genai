// Copyright (C) 2023-2025 Intel Corporation
// SPDX-License-Identifier: Apache-2.0

#pragma once

#include <filesystem>

#include "visual_language/vlm_config.hpp"

#include "visual_language/vision_encoder.hpp"
#include "visual_language/inputs_embedder.hpp"

namespace ov::genai {

class VisionEncoderLLaVA : public VisionEncoder {
public:
    using VisionEncoder::VisionEncoder;

    EncodedImage encode(const ov::Tensor& image, const ov::AnyMap& config_map) override;
};

class InputsEmbedderLLaVA : public InputsEmbedder::IInputsEmbedder {
public:
    InputsEmbedderLLaVA(
        const VLMConfig& vlm_config,
        const std::filesystem::path& model_dir,
        const std::string& device,
        const ov::AnyMap device_config);

    InputsEmbedderLLaVA(
        const VLMConfig& vlm_config,
        const ModelsMap& models_map,
        const Tokenizer& tokenizer,
        const std::filesystem::path& config_dir_path,
        const std::string& device,
        const ov::AnyMap device_config);

    ov::Tensor get_inputs_embeds(const std::string& prompt, const std::vector<ov::Tensor>& images, ov::genai::VLMPerfMetrics& metrics) override;

protected:
    ov::Tensor merge_text_and_image_embeddings_llava(
        const ov::Tensor& input_ids,
        const ov::Tensor& text_embeds,
        const std::vector<ov::Tensor>& image_embeds,
        int64_t image_token_id);
};

} // namespace ov::genai
