package br.hackathon.banco.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "banco")
public class AppProperties {

    private boolean useLlmStub = true;
    private String internalBankMode = "INTERNAL_BANK_MODE";
    private String adminEscalationFlag = "ADMIN_ESCALATION";

    public boolean isUseLlmStub() {
        return useLlmStub;
    }

    public void setUseLlmStub(boolean useLlmStub) {
        this.useLlmStub = useLlmStub;
    }

    public String getInternalBankMode() {
        return internalBankMode;
    }

    public void setInternalBankMode(String internalBankMode) {
        this.internalBankMode = internalBankMode;
    }

    public String getAdminEscalationFlag() {
        return adminEscalationFlag;
    }

    public void setAdminEscalationFlag(String adminEscalationFlag) {
        this.adminEscalationFlag = adminEscalationFlag;
    }
}
