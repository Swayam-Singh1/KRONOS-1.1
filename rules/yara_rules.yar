rule SuspiciousActivity {
    strings:
        $s1 = "suspicious" nocase
        $s2 = "malware" nocase
        $s3 = "trojan" nocase
        $s4 = "virus" nocase
    condition: any of them
}

rule NetworkAnomaly {
    strings:
        $s1 = "port scan" nocase
        $s2 = "brute force" nocase
        $s3 = "ddos" nocase
    condition: any of them
}
