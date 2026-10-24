from django import forms


class ProofForm(forms.Form):
    # Optional delivery photo; ImageField also checks the file is a real image.
    proof = forms.ImageField(required=False)

    def clean_proof(self):
        proof = self.cleaned_data.get("proof")
        if proof and proof.size > 3 * 1024 * 1024:
            raise forms.ValidationError("Photo must be smaller than 3 MB.")
        return proof
