@login_required
def create_tournament(request):
    if request.user.role != 'organizer':
        messages.error(request, "Only organizers can create tournaments.")
        return redirect('tournament_list')

    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament           = form.save(commit=False)
            tournament.organizer = request.user
            tournament.status    = 'pending'

            venue      = form.cleaned_data.get('venue')
            start_date = form.cleaned_data.get('start_date')
            end_date   = form.cleaned_data.get('end_date')

            # ── Check if venue is already booked on overlapping dates ──
            if venue and start_date and end_date:

                # Check against standalone venue bookings
                booking_conflict = VenueBooking.objects.filter(
                    venue=venue,
                    status__in=['pending', 'confirmed'],
                    start_date__lte=end_date,
                    end_date__gte=start_date,
                ).exists()

                # Check against other tournaments at same venue
                tournament_conflict = Tournament.objects.filter(
                    venue=venue,
                    status__in=['pending', 'active', 'ongoing'],
                    start_date__lte=end_date,
                    end_date__gte=start_date,
                ).exists()

                if booking_conflict or tournament_conflict:
                    messages.error(
                        request,
                        f"⚠️ '{venue.name}' is already booked between "
                        f"{start_date} and {end_date}. "
                        f"Please choose different dates."
                    )
                    return render(request, 'tournaments/tournament_form.html', {
                        'form': form, 'title': 'Create Tournament',
                    })

            # ── Set payment info based on venue ──
            if venue and venue.requires_payment:
                tournament.venue_payment_required = True
                tournament.venue_payment_amount   = venue.payment_amount
                tournament.venue_payment_code     = f"TRN-{uuid.uuid4().hex[:8].upper()}"
            else:
                tournament.venue_payment_required = False
                tournament.venue_payment_amount   = 0.00
                tournament.venue_payment_code     = ''

            tournament.save()
            messages.success(request, f"Tournament '{tournament.name}' submitted for admin approval.")

            # ── Go to payment page if payment needed, otherwise go to detail ──
            if tournament.venue_payment_required:
                return redirect('tournament_payment_info', pk=tournament.pk)

            return redirect('tournament_detail', pk=tournament.pk)

    else:
        form = TournamentForm()

    return render(request, 'tournaments/tournament_form.html', {
        'form': form, 'title': 'Create Tournament',
    })
