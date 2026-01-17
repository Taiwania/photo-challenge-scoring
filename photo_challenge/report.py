def generate_mw_table(results, stats):
    out = []
    out.append(f"*Number of contributors: {stats['contributors']}")
    out.append(f"*Number of voters:       {stats['voters']}")
    out.append(f"*Number of images:       {stats['images']}")
    out.append("")
    out.append("The Score is the sum of the 3*/2*/1* votes. The Support is the count of 3*/2*/1* votes and 0* likes. In the event of a tie vote, the support decides the rank.")
    out.append("")
    out.append('{| class="sortable wikitable"')
    out.append('|-')
    out.append('! class="unsortable"| Image')
    out.append('! Author')
    out.append('! data-sort-type="number" | Rank')
    out.append('! data-sort-type="number" | Score')
    out.append('! data-sort-type="number" | Support')
    
    current_rank = 1
    for i, res in enumerate(results):
        rank = i + 1
        if i > 0:
            prev = results[i-1]
            if prev['score'] == res['score'] and prev['support'] == res['support']:
                rank = current_rank
            else:
                current_rank = rank
        else:
            current_rank = rank

        img_cell = f"[[File:{res['filename']}|120px]]"
        auth_cell = f"[[User:{res['author']}|{res['author']}]] ([[User talk:{res['author']}|<span class=\"signature-talk\">talk</span>]])" if res['author'] != "Unknown" else "Unknown"
        
        row = "|-\n"
        row += f"| {img_cell} || {auth_cell} || {current_rank} || {res['score']} || {res['support']}"
        out.append(row)
        
    out.append('|}')
    return "\n".join(out)
