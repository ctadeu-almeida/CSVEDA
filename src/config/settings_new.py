# -*- coding: utf-8 -*-
"""
Settings - Sistema de configurações com Pydantic

Este módulo gerencia todas as configurações da aplicação usando
python-decouple e Pydantic para validação e tipagem.
"""

from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseSettings, Field, validator
from decouple import config
import os


class GeminiSettings(BaseSettings):
    """Configurações do Google Gemini"""

    model: str = Field(default="gemini-2.5-flash", description="Modelo Gemini a usar")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="Temperatura do modelo")
    max_output_tokens: int = Field(default=8192, gt=0, description="Máximo de tokens de saída")
    max_retries: int = Field(default=3, ge=0, description="Máximo de tentativas")
    request_timeout: int = Field(default=60, gt=0, description="Timeout em segundos")

    @validator('temperature')
    def validate_temperature(cls, v):
        """Validar temperatura entre 0 e 2"""
        if not 0.0 <= v <= 2.0:
            raise ValueError('Temperature must be between 0.0 and 2.0')
        return v


class MistralSettings(BaseSettings):
    """Configurações do Mistral via Ollama"""

    model: str = Field(default="mistral:latest", description="Modelo Mistral a usar")
    base_url: str = Field(default="http://localhost:11434", description="URL base do Ollama")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="Temperatura do modelo")


class AgentSettings(BaseSettings):
    """Configurações dos agentes LangChain"""

    max_iterations: int = Field(default=15, gt=0, description="Máximo de iterações")
    max_execution_time: int = Field(default=120, gt=0, description="Tempo máximo de execução")
    early_stopping_method: Literal["force", "generate"] = Field(
        default="force",
        description="Método de parada antecipada"
    )


class DataSettings(BaseSettings):
    """Configurações de processamento de dados"""

    max_csv_size_mb: int = Field(default=100, gt=0, description="Tamanho máximo do CSV em MB")
    chart_detection_window_seconds: int = Field(
        default=120,
        gt=0,
        description="Janela de detecção de gráficos em segundos"
    )
    charts_dir: str = Field(default="charts", description="Diretório para gráficos")
    reports_dir: str = Field(default="reports", description="Diretório para relatórios")
    pandas_chunk_size: int = Field(default=10000, gt=0, description="Tamanho do chunk do pandas")


class LoggingSettings(BaseSettings):
    """Configurações de logging"""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Nível de log"
    )
    retention_days: int = Field(default=30, gt=0, description="Dias de retenção dos logs")
    max_size_mb: int = Field(default=10, gt=0, description="Tamanho máximo do arquivo de log")


class SecuritySettings(BaseSettings):
    """Configurações de segurança"""

    session_timeout_minutes: int = Field(
        default=60,
        gt=0,
        description="Timeout da sessão em minutos"
    )
    max_upload_size_mb: int = Field(
        default=200,
        gt=0,
        description="Tamanho máximo de upload em MB"
    )


class AppSettings(BaseSettings):
    """Configurações principais da aplicação"""

    # Informações da aplicação
    name: str = Field(default="CSVEDA", description="Nome da aplicação")
    version: str = Field(default="1.0.0", description="Versão da aplicação")
    debug: bool = Field(default=False, description="Modo debug")
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Ambiente de execução"
    )

    # API Keys
    google_api_key: Optional[str] = Field(default=None, description="Chave da API Google")
    openai_api_key: Optional[str] = Field(default=None, description="Chave da API OpenAI")

    # Configurações específicas
    gemini: GeminiSettings = Field(default_factory=GeminiSettings)
    mistral: MistralSettings = Field(default_factory=MistralSettings)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    data: DataSettings = Field(default_factory=DataSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator('google_api_key', pre=True)
    def get_google_api_key(cls, v):
        """Obter Google API Key do ambiente"""
        return v or config('GOOGLE_API_KEY', default=None)

    @validator('openai_api_key', pre=True)
    def get_openai_api_key(cls, v):
        """Obter OpenAI API Key do ambiente"""
        return v or config('OPENAI_API_KEY', default=None)

    def setup_directories(self):
        """Criar diretórios necessários"""
        dirs_to_create = [
            self.data.charts_dir,
            self.data.reports_dir,
            "logs",
            "temp"
        ]

        for dir_name in dirs_to_create:
            Path(dir_name).mkdir(exist_ok=True)

    def get_model_config(self, model_type: str) -> dict:
        """Obter configuração específica do modelo"""
        if model_type.lower() == "gemini":
            return {
                "model": self.gemini.model,
                "temperature": self.gemini.temperature,
                "max_output_tokens": self.gemini.max_output_tokens,
                "max_retries": self.gemini.max_retries,
                "request_timeout": self.gemini.request_timeout,
                "api_key": self.google_api_key
            }
        elif model_type.lower() == "mistral":
            return {
                "model": self.mistral.model,
                "base_url": self.mistral.base_url,
                "temperature": self.mistral.temperature
            }
        else:
            raise ValueError(f"Modelo não suportado: {model_type}")


# Instância global das configurações
new_settings = AppSettings()

# Função de conveniência para obter configurações
def get_new_settings() -> AppSettings:
    """Retorna a instância global das configurações"""
    return new_settings

# Função para setup inicial
def setup_directories_new():
    """Criar diretórios necessários"""
    new_settings.setup_directories()

# Compatibilidade com código existente
def get_model_config_new(model_type: str) -> dict:
    """Obter configuração do modelo (nova versão)"""
    return new_settings.get_model_config(model_type)