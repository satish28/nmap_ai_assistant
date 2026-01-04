import click
import ollama


"""
Local LLM Smart Scanner: 

Given an Nmap Scan Output - 

All_scan - Analyse Open ports and Services. Use LLM to get insights about the host. Find CVE's for identified services. Find any public exploits available.
For identified services what give references to what type of attacks can be tested. 
"""
sec_engineer = """I am a Senior Network Security Engineer, in charge of securing my org’s internal and external networks."""

def ai_llm_integrtation(nmap_file, special_prompt, model):
    
    llm_prompt = sec_engineer + nmap_file + special_prompt
    for chunk in ollama.generate(model=model, prompt=llm_prompt ,stream=True):
        print(chunk['response'], end='', flush=True)

def all_scan(nmap_file, model):
    analyse(nmap_file, model)
    cve_finder(nmap_file, model)
    exploit_finder(nmap_file, model)
    share_test_plan(nmap_file, model)

# Analyse the nmap results and provide insights into the kind of host
def analyse(nmap_file, model):
    special_prompt = """Based on the Nmap scan output provided - provide insights about the host from Security aspect."""
    print(ai_llm_integrtation(nmap_file, special_prompt, model)) 

# Find public CVEs based on the services identified
def cve_finder(nmap_file, model):
    special_prompt = """Given the nmap scan output - for all open services list out any available CVEs as a table.."""
    print(ai_llm_integrtation(nmap_file, special_prompt, model)) 

# Find public exploits available based on the services identified 
def exploit_finder(nmap_file, model):
    special_prompt = """Given the nmap scan output - for all open services list out public exploits as a table."""
    print(ai_llm_integrtation(nmap_file, special_prompt, model)) 

# Based on the identified servies what kind of attacks do i need to test for.
def share_test_plan(nmap_file, model):
    special_prompt = """One of my tasks is to review NMAP scans and create test plans for services identified for a host. Given the nmap scan output - suggest test plans and share links to documentation."""
    print(ai_llm_integrtation(nmap_file, special_prompt, model))


@click.group()
@click.option(
    "--model",
    default="gemma3:4b",
    show_default=True,
    help="LLM model to use for all commands"
)
@click.pass_context
def cli(ctx, model):
    ctx.ensure_object(dict)
    ctx.obj["model"] = model


@cli.command('all')
@click.argument('nmap_file')
@click.pass_context
def all_scan_cli(ctx, nmap_file):
    """Performs a comprehensive Nmap scan."""
    with open(nmap_file, "r") as f:
        read_nmap_file = f.read()
    model = ctx.obj["model"]
    all_scan(read_nmap_file, model)


@cli.command('smart')
@click.argument('nmap_file')
@click.pass_context
def analyse_cli(ctx, nmap_file):
    """Performs a smart Nmap scan."""
    with open(nmap_file, "r") as f:
        read_nmap_file = f.read()
    
    model = ctx.obj["model"]
    analyse(read_nmap_file, model)


@cli.command('cve')
@click.argument('nmap_file')
@click.pass_context
def cve_scan(ctx, nmap_file):
    """Scans for CVE vulnerabilities."""
    with open(nmap_file, "r") as f:
        read_nmap_file = f.read()
    
    model = ctx.obj["model"]
    cve_finder(read_nmap_file, model)

@cli.command('exploit')
@click.argument('nmap_file')
@click.pass_context
def exploit_scan(ctx, nmap_file):
    """Attempts to exploit identified vulnerabilities."""
    with open(nmap_file, "r") as f:
        read_nmap_file = f.read()
    model = ctx.obj["model"]
    exploit_finder(read_nmap_file, model)

@cli.command('assist')
@click.argument('nmap_file')
@click.pass_context
def assist_scan(ctx, nmap_file):
    """Provides assistance and guidance based on scan results."""
    with open(nmap_file, "r") as f:
        read_nmap_file = f.read()
    model = ctx.obj["model"]
    share_test_plan(read_nmap_file, model)

if __name__ == '__main__':
    cli()